class Callback():
    def reset(self):  raise NotImplementedError
    def update(self): raise NotImplementedError
    
    def __repr__ (self) -> str:
        return f'{self.__class__.__name__}()'


class LoggerCallback(Callback):
    preset_structure = {
        'ammos':   {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 0, 'Infos'], 'id_key': 'Name'},
        'pickups': {'path': ['CPickupDataManager', 'pickupData'], 'id_key': 'Name'},
    }
    
    def __init__(self, structure:dict|str):
        if isinstance(structure, str):
            assert structure in self.preset_structure.keys(), f'Invalid structure key: {structure}'
            self.structure = self.preset_structure[structure]
        self.reset()

    def update(self, new_items:list, metadata:dict):
        for item in new_items:
            log_item = {k:v for k, v in metadata.items()}
            item_id = item[self.structure['id_key']]
            if item_id in self.items.keys():
                self.items[item_id].update(log_item)
            else:
                self.items[item_id] = log_item

    def reset(self):
        self.items:dict[str, dict] = {}
    
    @property
    def data(self) -> dict[str, dict]:
        return self.items


class WeaponLoggerCallback(Callback):
    def __init__(self):
        self.structure = {'path': ['CWeaponInfoBlob', 'Infos', 'Item', 1, 'Infos'], 'id_key': 'Name'}
        self.reset()
    
    def update(self, new_items:list, metadata:dict):
        for item in new_items:
            log_item = {
                'AmmoInfo': item['AmmoInfo']['@ref'],
                **metadata
            }
            item_id = item[self.structure['id_key']]
            if item_id in self.items.keys():
                self.items[item_id].update(log_item)
            else:
                self.items[item_id] = log_item
    
    def reset(self):
        self.items:dict[str, dict] = {}
    
    @property
    def data(self) -> dict[str, dict]:
        return self.items