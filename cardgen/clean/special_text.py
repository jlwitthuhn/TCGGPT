from .strings import (
    NAMED_CARD,
    NAMED_PERMANENT,
    SELF,
    UNIQUE_COUNTER,
    UNIQUE_PLANESWALKER_TYPE,
)

_SPECIAL_CASES = {}
# Remove this if a third basri is added
_SPECIAL_CASES["adherent of hope"] = [
    ("basri", UNIQUE_PLANESWALKER_TYPE),
]
_SPECIAL_CASES["aisha of sparks and smoke"] = [
    ("aisha", SELF),
]
_SPECIAL_CASES["ajani, strength of the pride"] = [
    ("~'s pridemate", NAMED_PERMANENT),
]
_SPECIAL_CASES["arbiter of the ideal"] = [
    ("manifestation", UNIQUE_COUNTER),
]
_SPECIAL_CASES["awakening of vitu-ghazi"] = [
    ("vitu-ghazi", NAMED_PERMANENT),
]
_SPECIAL_CASES["behemoth's herald"] = [
    ("godsire", NAMED_CARD),
]
_SPECIAL_CASES["boris devilboon"] = [
    ("minor demon", NAMED_PERMANENT),
]
_SPECIAL_CASES["catti-brie of mithral hall"] = [
    ("catti-brie", SELF),
]
_SPECIAL_CASES["chandra's outburst"] = [
    ("chandra, bold pyromancer", NAMED_PERMANENT),
]
_SPECIAL_CASES["denry klin, editor in chief"] = [
    ("denry", SELF),
]
_SPECIAL_CASES["drizzt do'urden"] = [
    ("guenhwyvar", NAMED_PERMANENT),
]
_SPECIAL_CASES["ellivere of the wild court"] = [
    ("virtuous", NAMED_PERMANENT),
]
_SPECIAL_CASES["estrid, the masked"] = [
    ("mask", NAMED_PERMANENT),
]
_SPECIAL_CASES["farid, enterprising salvager"] = [
    ("scrap", NAMED_PERMANENT),
]
_SPECIAL_CASES["garth one-eye"] = [
    ("terror", NAMED_CARD),
]
_SPECIAL_CASES["general kudro of drannith"] = [
    ("general kudro", SELF),
]
_SPECIAL_CASES["giant caterpillar"] = [
    ("butterfly", NAMED_PERMANENT),
]
_SPECIAL_CASES["goldmeadow lookout"] = [
    ("goldmeadow harrier", NAMED_PERMANENT),
]
_SPECIAL_CASES["helm of kaldra"] = [
    ("kaldra", NAMED_PERMANENT),
]
_SPECIAL_CASES["inquisitor eisenhorn"] = [
    ("cherubael", NAMED_PERMANENT),
]
_SPECIAL_CASES["jedit ojanen of efrava"] = [
    ("jedit ojanen", SELF),
]
_SPECIAL_CASES["kaya the inexorable"] = [
    ("ghostform", UNIQUE_COUNTER),
]
_SPECIAL_CASES["kibo, uktabi prince"] = [
    ("banana", NAMED_PERMANENT),
]
_SPECIAL_CASES["kjeldoran home guard"] = [
    ("deserter", NAMED_PERMANENT),
]
_SPECIAL_CASES["koma, cosmos serpent"] = [
    # Actually named "koma's coil" but the name has already been replaced
    ("~'s coil", NAMED_PERMANENT),
]
_SPECIAL_CASES["koma, world-eater"] = [
    # Actually named "koma's coil" but the name has already been replaced
    ("~'s coil", NAMED_PERMANENT),
]
_SPECIAL_CASES["kyscu drake"] = [
    ("spitting drake", NAMED_PERMANENT),
]
_SPECIAL_CASES["lita, mechanical engineer"] = [
    ("zeppelin", NAMED_PERMANENT),
]
_SPECIAL_CASES["llanowar mentor"] = [
    ("llanowar elves", NAMED_PERMANENT),
]
_SPECIAL_CASES["mangara of corondor"] = [
    ("mangara", SELF),
]
_SPECIAL_CASES["mishra, eminent one"] = [
    ("~'s warform", NAMED_PERMANENT),
]
_SPECIAL_CASES["murmuration"] = [
    ("storm crow", NAMED_PERMANENT),
]
_SPECIAL_CASES["moira brown, guide author"] = [
    ("wasteland survival guide", NAMED_PERMANENT),
]
_SPECIAL_CASES["nazahn, revered bladesmith"] = [
    ("hammer of ~", NAMED_PERMANENT),
]
_SPECIAL_CASES["nesting dragon"] = [
    ("dragon egg", NAMED_PERMANENT),
]
_SPECIAL_CASES["overlord of the hauntwoods"] = [
    ("everywhere", NAMED_PERMANENT),
]
_SPECIAL_CASES["palani's hatcher"] = [
    ("dinosaur egg", NAMED_PERMANENT),
]
_SPECIAL_CASES["phantasmal sphere"] = [
    ("orb", NAMED_PERMANENT),
]
_SPECIAL_CASES["replicating ring"] = [
    ("replicated ring", NAMED_PERMANENT),
]
_SPECIAL_CASES["sharae of numbing depths"] = [
    ("sharae", SELF),
]
_SPECIAL_CASES["sliversmith"] = [
    ("metallic sliver", NAMED_PERMANENT),
]
_SPECIAL_CASES["smoke spirits' aid"] = [
    ("smoke blessing", NAMED_PERMANENT),
]
_SPECIAL_CASES["sophia, dogged detective"] = [
    ("tiny", NAMED_PERMANENT),
]
_SPECIAL_CASES["sothera, the supervoid"] = [
    ("sothera", SELF),
]
_SPECIAL_CASES["splintering wind"] = [
    ("splinter", NAMED_PERMANENT),
]
_SPECIAL_CASES["summoning station"] = [
    ("pincher", NAMED_PERMANENT),
]
_SPECIAL_CASES["svella, ice shaper"] = [
    ("icy manalith", NAMED_PERMANENT),
]
_SPECIAL_CASES["tetravus"] = [
    ("tetravite", NAMED_PERMANENT),
]
_SPECIAL_CASES["tezzeret the schemer"] = [
    ("etherium cell", NAMED_PERMANENT),
]
_SPECIAL_CASES["the eleventh hour"] = [
    ("prisoner zero", NAMED_PERMANENT),
]
_SPECIAL_CASES["the first doctor"] = [
    ("tardis", NAMED_CARD),
]
_SPECIAL_CASES["the hive"] = [
    ("wasp", NAMED_PERMANENT),
]
_SPECIAL_CASES["the rani"] = [
    ("mark of the rani", NAMED_PERMANENT),
]
_SPECIAL_CASES["the spear of leonidas"] = [
    ("phobos", NAMED_PERMANENT),
]
_SPECIAL_CASES["tomb of urami"] = [
    ("urami", NAMED_PERMANENT),
]
_SPECIAL_CASES["tooth and claw"] = [
    ("carnivore", NAMED_PERMANENT),
]
_SPECIAL_CASES["triskelavus"] = [
    ("triskelavite", NAMED_PERMANENT),
]
_SPECIAL_CASES["tuktuk the explorer"] = [
    ("tuktuk the returned", NAMED_PERMANENT),
]
_SPECIAL_CASES["twitching doll"] = [
    ("nest", UNIQUE_COUNTER),
]
_SPECIAL_CASES["verix bladewing"] = [
    ("karox bladewing", NAMED_PERMANENT),
]
_SPECIAL_CASES["wall of kelp"] = [
    ("kelp", NAMED_PERMANENT),
]
_SPECIAL_CASES["weapons manufacturing"] = [
    ("munitions", NAMED_PERMANENT),
]
_SPECIAL_CASES["witness protection"] = [
    ("legitimate businessperson", NAMED_PERMANENT),
]
_SPECIAL_CASES["xathrid gorgon"] = [
    ("petrification", UNIQUE_COUNTER),
]
_SPECIAL_CASES["zimone, all-questioning"] = [
    ("primo, the indivisible", NAMED_PERMANENT),
]


def clean_special_text(the_card: dict):
    if the_card["name"] in _SPECIAL_CASES:
        for find, replace in _SPECIAL_CASES[the_card["name"]]:
            the_card["oracle_text"] = the_card["oracle_text"].replace(find, replace)
