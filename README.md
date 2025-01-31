# weapon-merger
Script to merge weapons data files in GTA V for modding | Version 1.2 | [gta5-mods.com](https://www.gta5-mods.com/tools/weapon-merger)

### What this script does:
**TLDR:** Merge all vanilla `weapon*.meta` and `pickups.meta` to a single file. **Merged files included.**
<details><summary>Details</summary>

1. Crawl list of all DLCs from latest `dlclist.xml`
2. Crawl list of all DLC patches from latest `extratitleupdatedata.meta`
3. Scan for all content.xml, weapon<...>.meta, pickups.meta files in all dlc archives
    + Other filetypes can be adapted by writing new parser in `./resources/parser.py`
4. Merge all vanilla `weapon*.meta` files and export to `outputs/merged/update/update.rpf/common/data/ai/weapons.meta`
5. Merge all vanilla `pickups.meta` files and export to `outputs/merged/update/update.rpf/common/data/pickups.meta`
6. Patch `content.xml` in every **processed** DLCs to deactivate loading of old weapon-.meta and pickups.meta and export them to `./outputs/merged/update/update.rpf/dlc_patch`
7. Export documents on list of dlcs, and list of weapons/ammos/pickups by DLC.
</details>

### Why/How it helps modding
+ GTA V weapons mods require tampering `weapon*.meta` and `pickups.meta` in every individual DLCs and their patches.
+ This means changes need to be made across multiple DLC archives, whichs makes modding extremely vulnerable to manual errors and costs huge amount of cloned/modded archives.
+ By merging them all to a single file/a few files, edits can be made in one place. Thus, less error and less wasted space.
+ This also makes patching multiple weapon mods together easier.

### How to run:
1. For end-users (who do not necessarily need this mod): Copy everything in `./composed/merged/update/update.rpf` to `GTA V/mods/update/update.rpf`.
    + This does not make any changes to vanilla weapons in-game.
2. For developers (target users of this mod):
    1. (Optional, Recommended): Install [miniconda](https://docs.anaconda.com/miniconda/install/)
    2. (Optional, Recommended): With installed conda, create environment from terminal `conda env create -f environment.yaml`
    3. (Optional, Recommended): Activate environment: `conda activate weapon-merger`
    4. Extract `weapons-pickups-meta-backup-1.70.7z` to current folder (same level as this file).
    5. Open `./main.ipynb` and run everything in one go. Merged files will be exported to `./outputs/merged`
3. Patch for LCPP: Copy `./composed/patch-lcpp/update/update.rpf/dlc_patch/mpheist4/content.xml` to `GTA V/mods/update/update.rpf/dlc_patch/mpheist4`

### Uninstall
1. Extract `weapons-pickups-meta-uninstall-1.70.7z` to current folder (same level as this file).
2. Open the `./composed/uninstall-content-dlcpatch.yaml` - This is the instruction to handle `content.xml` in each `dlc_patch`
3. Copy everything in `./uninstall/update/update.rpf` to  `GTA V/mods/update/update.rpf`
    + These should have reverted the DLCs under `to-patch` in `./composed/uninstall-content-dlcpatch.yaml`
4. For the remaining DLCs, i.e. under `to-delete` in `./composed/uninstall-content-dlcpatch.yaml`, you can safely delete the `content.xml` file manually.
    + Originally these files do not exist in the vanilla version
