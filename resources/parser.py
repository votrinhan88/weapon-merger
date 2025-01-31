from typing import Sequence

import xml.etree.ElementTree as ET
import xmltodict

from .callbacks import LoggerCallback, WeaponLoggerCallback


def traverse_xmldict(input:dict, keys:Sequence[str], strict:bool=False):
    """Traverses a nested dictionary using a list of keys.

    Args:
    + input (dict): The dictionary to traverse.
    + keys (Sequence[str]): A list of keys representing the traversal path.

    Returns:
    + The value at the specified path or None if the path does not exist.
    
    Examples:
    >>> a = {'b': {'c': {'d': {'e': 0}}}}
    >>> traverse_xmldict(input=a, keys=['b', 'c', 'd', 'e'])
    0
    >>> traverse_xmldict(input=a, keys=['b', 'f'])
    None
    """
    current = input
    for k in keys:
        if isinstance(current, (dict)) and k in current.keys():
            current = current[k]
        elif isinstance(current, Sequence):
            current = current[k]
        else:
            if strict:
                raise ValueError(f'Could not find key `{k}` for input {input}')
            else:
                return None  # Return None if the path does not exist
    return current


class Parser():    
    def __init__(self, template_source:str):
        self.template_source = template_source
        self.reset()

    @staticmethod
    def parse_xmltodict(source:str) -> dict:
        return xmltodict.parse(ET.tostring(ET.parse(source=source).getroot()))
    
    def __repr__ (self) -> str:
        return f'{self.__class__.__name__}(template_source={self.template_source})'
    
    def reset():
        raise NotImplementedError('Method `reset` must be implemented by subclasses.')
    
    def update(self, new:dict, metadata:dict):
        raise NotImplementedError('Method `update` must be implemented by subclasses.')


class WeaponMetaParser(Parser):
    traverse_suffix = ['Item']
    
    def reset(self):
        self.template = self.parse_xmltodict(source=self.template_source)
        self.structure = {
            'SlotNavigateOrder': {
                0: {'path': ['CWeaponInfoBlob', 'SlotNavigateOrder', 'Item', 0, 'WeaponSlots'], 'id_key': 'Entry', 'unique_ids': []},
                1: {'path': ['CWeaponInfoBlob', 'SlotNavigateOrder', 'Item', 1, 'WeaponSlots'], 'id_key': 'Entry', 'unique_ids': []},
            },
            'SlotBestOrder': {'path': ['CWeaponInfoBlob', 'SlotBestOrder', 'WeaponSlots'], 'id_key': 'Entry', 'unique_ids': []},
            'TintSpecValues': {'path': ['CWeaponInfoBlob', 'TintSpecValues'], 'id_key': 'Name', 'unique_ids': []},
            'FiringPatternAliases': {'path': ['CWeaponInfoBlob', 'FiringPatternAliases'], 'id_key': 'Name', 'unique_ids': []},
            'UpperBodyFixupExpressionData': {'path': ['CWeaponInfoBlob', 'UpperBodyFixupExpressionData'], 'id_key': 'Name', 'unique_ids': []},
            'AimingInfos': {'path': ['CWeaponInfoBlob', 'AimingInfos'], 'id_key': 'Name', 'unique_ids': []},
            'Infos': {
                0: {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 0, 'Infos'], 'id_key': 'Name', 'unique_ids': [], 'callbacks': [LoggerCallback(structure='ammos')]},
                1: {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 1, 'Infos'], 'id_key': 'Name', 'unique_ids': [], 'callbacks': [WeaponLoggerCallback()]},
                2: {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 2, 'Infos'], 'id_key': 'Name', 'unique_ids': []},
                3: {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 3, 'Infos'], 'id_key': 'Name', 'unique_ids': []},
            },
            'VehicleWeaponInfos': {'path': ['CWeaponInfoBlob', 'VehicleWeaponInfos'], 'id_key': 'Name', 'unique_ids': []},
            'WeaponGroupDamageForArmouredVehicleGlass': {'path': ['CWeaponInfoBlob', 'WeaponGroupDamageForArmouredVehicleGlass'], 'id_key': 'GroupHash', 'strict': False, 'unique_ids': []},
        }
        for st in [
            self.structure['SlotNavigateOrder'][0],
            self.structure['SlotNavigateOrder'][1],
            self.structure['SlotBestOrder'],
            self.structure['TintSpecValues'],
            self.structure['FiringPatternAliases'],
            self.structure['UpperBodyFixupExpressionData'],
            self.structure['AimingInfos'],
            self.structure['Infos'][0],
            self.structure['Infos'][1],
            self.structure['Infos'][2],
            self.structure['Infos'][3],
            self.structure['VehicleWeaponInfos'],
            self.structure['WeaponGroupDamageForArmouredVehicleGlass'],
        ]:
            items = traverse_xmldict(input=self.template, keys=st['path']+self.traverse_suffix)
            for item in items:
                st['unique_ids'].append(item[st['id_key']])
            
    def update(self, new:dict, metadata:dict):
        for st in [
            self.structure['SlotNavigateOrder'][0],
            self.structure['SlotNavigateOrder'][1],
            self.structure['SlotBestOrder'],
            self.structure['TintSpecValues'],
            self.structure['FiringPatternAliases'],
            self.structure['UpperBodyFixupExpressionData'],
            self.structure['AimingInfos'],
            self.structure['Infos'][0],
            self.structure['Infos'][1],
            self.structure['Infos'][2],
            self.structure['Infos'][3],
            self.structure['VehicleWeaponInfos'],
            # self.structure['WeaponGroupDamageForArmouredVehicleGlass'],
        ]:
            has_items = (traverse_xmldict(input=new, keys=st['path']) is not None)
            if has_items:
                new_items = traverse_xmldict(input=new, keys=st['path']+self.traverse_suffix)
                if isinstance(new_items, dict):
                    new_items = [new_items]
                
                old_items = traverse_xmldict(input=self.template, keys=st['path']+self.traverse_suffix)
                for ni in new_items:
                    new_item_id = ni[st['id_key']]
                    if new_item_id in st['unique_ids']:
                        idx_duplicate = st['unique_ids'].index(new_item_id)
                        old_items[idx_duplicate] = ni
                    else:
                        old_items.append(ni)
                        st['unique_ids'].append(new_item_id)

                if st.get('callbacks') is not None:
                    for cb in st['callbacks']:
                        # Do something here
                        cb.update(new_items=new_items, metadata=metadata)
    
    @property
    def data(self) -> dict[str, dict]:
        return self.template


class PickupsMetaParser(Parser):
    traverse_suffix = ['Item']
    
    def __init__(self, template_source:str):
        self.template_source = template_source
        self.reset()
    
    def reset(self):
        self.template = self.parse_xmltodict(source=self.template_source)
        self.structure = {
            'pickupData': {'path': ['CPickupDataManager', 'pickupData'], 'id_key': 'Name', 'unique_ids': [], 'callbacks': [LoggerCallback(structure='pickups')]},
            'actionData': {'path': ['CPickupDataManager', 'actionData'], 'id_key': 'Name', 'unique_ids': []},
            'rewardData': {'path': ['CPickupDataManager', 'rewardData'], 'id_key': 'Name', 'unique_ids': []},
        }
        for st in [
            self.structure['pickupData'],
            self.structure['actionData'],
            self.structure['rewardData'],
        ]:
            items = traverse_xmldict(input=self.template, keys=st['path']+self.traverse_suffix)
            for item in items:
                st['unique_ids'].append(item[st['id_key']])
            
    def update(self, new:dict, metadata:dict):
        for st in [
            self.structure['pickupData'],
            self.structure['actionData'],
            self.structure['rewardData'],
        ]:
            has_items = (traverse_xmldict(input=new, keys=st['path']) is not None)
            if has_items:
                new_items = traverse_xmldict(input=new, keys=st['path']+self.traverse_suffix)
                if isinstance(new_items, dict):
                    new_items = [new_items]
                
                old_items = traverse_xmldict(input=self.template, keys=st['path']+self.traverse_suffix)
                for ni in new_items:
                    new_item_id = ni[st['id_key']]
                    if new_item_id in st['unique_ids']:
                        idx_duplicate = st['unique_ids'].index(new_item_id)
                        old_items[idx_duplicate] = ni
                    else:
                        old_items.append(ni)
                        st['unique_ids'].append(new_item_id)

                if st.get('callbacks') is not None:
                    for cb in st['callbacks']:
                        # Do something here
                        cb.update(new_items=new_items, metadata=metadata)
    
    @property
    def data(self) -> dict[str, dict]:
        return self.template