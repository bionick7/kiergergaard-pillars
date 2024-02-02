import os, sys
import regex as re

core_bonus = [
    "INTERVENTION DISPATCH",
    "OPTIMISED SMALL ARMS ASSORTMENT",
    "EMERGENCY FOAM",
    "PARTIAL COMPATIBILITY",
    "REACTOR SAFETY REDUNDANCY",
    "READINESS RESET",
    "BLACK MARKET TELEPORTER",
    "BLINK PATCH",
    "COMPRESSED CLOUDKILL PACK",
    "MOBILE INFANTRY COORDINATION",
    "LEUCOCYTE CODE",
    "INNOVATION CALCULATOR",
    "INTEREST WAR SHRAPNEL",
    "HERCYNIAN CRISIS AMMO STOCKPILES",
    "PURGATORY SUPER NAPALM",
    "EXPERIMENTAL VALVE",
    "UNAPPROVED CASINGS",
    "LIQUID NHP",
    "HIGH FREQUENCY CYCLING",
    "HIGH PERFORMANCE STANDARDS",
    "HIGH VELOCITY COMBATANT",
    "FULL BROADSIDE",
    "CROWSNEST BACKUP",
    "ARMOURED MUTINY",
]

frames = [
    "MIDZOR",
    "ATTAKULLA",
    "KILIMANJARO",
    "COLLAO",
    "ULURU",
    "GALDHØPIGGEN",
    "MAUNA KEA",
    "CHANG JIANG",
    "ORINOCO",
    "MISSISSIPPI",
    "YUKON",
    "URAL",
    "PANAMA",
    "AWAASH",
    "ACONCAGUA",
    "MAYON",
    "NGALIEMA",
    "DANUBE",
    "SEINE",
    "KONGO",
    "CHARLEMAGNE",
    "SCHWARZKOPF",
    "BOLIVAR",
    "COLUMBUS",
    "JANSZOON",
    "AMUNDSEN",
]

mods = [
    "NIGHTHAWK SCOPE",
    "DELAYED HIGH EXPLOSIVES",
    "LASER FOCUS CONVERTER",
    "POSTPONED EDGE PULSE",
    "BUCKSHOT",
    "SCRAP HARDENER",
    "HYPNOS FLASH",
    "BARBARA CLASS NHP",
    "HOMERUN LAUNCH PLATFORM",
    "QUEBEC SMOKE CANISTERS",
    "LUXEMBOURG-PATTERN BIPOD",
]

pilot_gear = [

]

systems = [
    "ABLATIVE BURNER PLATES",
    "AGGRESSIVE FLUSH SYSTEM LINKAGE",
    "AMBUSH PACK",
    "ANTI FRAME BARRICADE",
    "DAMPENER SHIELD",
    "DARTS-UI CONTROLS",
    "DIGITAL RIGHTS MANAGEMENT",
    "DOMOVOY NHP",
    "DROPTROOPER SUPPORT",
    "ESCAPE TOOL",
    "FIRE DUPLICATION BUG",
    "FIREWALL MANIFESTATION",
    "GIBRALTAR BARBED WIRE DRUMS",
    "METEOROLOGICAL SIMULATION",
    "MILORG REMOVAL DEVICE",
    "OOBD-SIGNAL",
    "ORBITAL GUIDANCE SCANNER",
    "PIGEON MINE LAUNCHER",
    "PILLBOX DRONE",
    "RADIATOR SHIELD",
    "RANGER CLOUD",
    "RESCUE CODE",
    "SATELLITE PLATING"
    "PACIFIER GAS MINES",
    "NITRO OVERDOSE",
    "BULLMOOSE DRONE",
    "PRISM SHIELD",
    "SUNRISE CHARGES",
    "GHOST DIVERSION",
    "WHISTLING SCARECROW",
    "SUNSET CHARGES",
    "SNOWFALL BEACON",
    "PLASMA CAPACITOR",
    "COOLANT SABOTAGE",
    "FORCED INSULATION",
    "SPARK CRACKER",
    "CARGO ROPEWAY",
    "SHELF BREAKER PUNCH",
    "PARABOLIC PUNCH",
    "ANALOGUE CONTROLS",
    "IMPROVISED EXPLOSIVE DEVICE",
    "SMART TARGETING RELAY",
    "TASK MANAGER SYSTEMS HALT",
    "THOR NHP",
    "VIRUTAL BACKDOOR",
    "WHITEWASH STIRRUP PUMP",
    "LIDAR TARGETING",
    "MOONLIGHT ARRIER DRONE",
    "EOE IMPACT LASER GRENADE",
    "SWIFT SERVOS",
    "WHITE HORSE ADVANCE",
    "IMPACT FIELD",
    "FACTORY PATTERN INTERCEPTOR",
    "CHAINS OF THE PROLETARIAT",
    "MAGFLOW",
    "PHASING BARRIER",
    "REDEPLOYMENT UI",
    "DISLIPA",
    "APOLLO CLASS NHP",
    "PRIORITY NEUTRALIZER",
    "ANTARES THERMITE",
    "SUBALTERN RAIDING SQUAD",
    "GILE MLRS",
    "TIMETABLE ENFORCEMENT",
    "NOBEL PRIMER",
    "BELL MINES",
    "FAITH OF MONIST-1",
    "JASY JATERE CLASS",
    "MORSE GUARDIAN",
    "CUCKOOSHRIKE NEEDLER",
    "STRIKE MELT",
    "CARABAO VIRAL PROTECTION",
    "PHYSICAL UPLINK",
    "HANDCUFF CODE",
    "AGGRESSIVE MEASURES",
    "SAFE HARBOUR LAMP",
    "BYPASS",
    "FORCEFUL PACIFICATION",
    "THBRRE EJECTOR",
    "AUTOLOADER CARROUSEL",
    "BOHR MINE",
    "FAILSAFE MELTDOWN",
    "TELLER DRONE",
    "M'BANZA CONSOLIDATION",
    "NOMAD DRONE",
    "NJAMBE CLASS NHP"
    "ROCKSOLID - EMERGENCY CLOAK",
    "TACTICAL OVERHEAT",
    "SHATTERSPRINGS JUMP",
    "SYSTEM",
    "FURNACE ARMOUR",
    "HARRISON'S BREATH",
    "ICARUS SUSPENSION",
    "REACTIVE IN-FLIGHT FLARES",
    "BLACK MARKET NITRO MIX",
    "CUIRASS DRONE",
    "HARD DRIVE GRUBBING",
    "GEO-LOCK TRIANGULATION",
    "STING RESPONDER",
    "PREDICTIVE MONITORING TOOL",
    "COUNTERSTRIKE DRONE",
    "MENRVA CLASS NHP",
    "ARMOURED NETWORK PROTOCOL",
    "BROADBAND JAMMER",
    "'PONG' HEAVY PING RADAR",
    "FOOL'S CODE",
    "SILENT NIGHT",
    "BUNKER BREACH CHARGES",
    "FRONTRUNNER BREACH SHIELD",
    "DISPOSABLE QUICK-CHANGE BARRELS",
]

talents = [

]

weapons = [
    "AHAB MISSILE",
    "AUTOCANNON",
    "BARNBUSTER HESH CANNON",
    "CHAINSAW",
    "COMPASS NEXUS",
    "FLASHFIRE CANNON",
    "HYDRAULIC RESCUE TOOL",
    "KRAKEN MACHINE GUN",
    "LASER GUIDED MISSILE",
    "LMG",
    "MACHINE CANNON",
    "MINITURISED SOLAR LANCE ",
    "PANZERBÜCHSE PHOSPHORUS BOXCUTTER",
    "RAPID FIRE MISSILE BATTERY",
    "SAM LAUNCHER",
    "SHIKISHIMA LASER RIFLE",
    "SMUGGLER'S FRIENDS",
    "SONIC BOOM WRECKING FLAIL",
    "SPEARTIP REPEATING CANNON",
    "TASER SHOTGUN",
    "THUNDERBREATH SHOTGUN",
    "TURN X BEAM CANNON",
    "WHITEWASH MONITOR",

    "TEARGAS LOBBER",
    "RAINBOW LAUNCHER",
    "PRECISION CROSSBOW",
    "SHARD CLOUD",
    "MANDARIN DARTS",
    "DJIBOUTI PATTERN COMPETITION REV.",
    "STALEMATE HAMMER",
    "GILE MLRS",
    "PUSH-PIN NEXUS",
    "CUCKOOSHRIKE NEEDLER",
    "HOPLOPHOBIA BATTLE RIFLE",
    "DARDANELLES RECOILLESS RIFLE",
    "LUCERNE SCREWDRIVER",
    "CHARGER FIRE LANCE",
    "GENDERAME 80MIL SPECIAL",
    "FLARE SABRE",
    "BOOM BARRIER NEXUS",
    "COUNSELLOR NEXUS",
    "SONIC BOOM WRECKING FLAIL",
    "THUNDERBREATH SHOTGUN",
    "FLASHFIRE CANNON",
    "PANZERBUECKSE BOXCUTTER",
    "TANDEM CHARGE RIFLE",
    "BARNBUSTER HESH CANNON",
    "AHAB-MISSILE",
    "COMPASS NEXUS",
    "RAPID FIRE MISSILE BATTERY",
    "WHALER REPEATING CANNON"
]

core_bonus_kian = [
    "Shinobi Stealth Module",
    "High-mobility Adaptation",
    "Heat Bleed Elimination",
    "Kata of the Short Blade",
    "Kata of the Sword",
    "Kata of Collective Dismemberment",
]

frames_kian = [
    "Harvester",
    "Chimaera",
    "Dismal Sylph",
    "Nue",
    "Gashadokuro",
    "Kitsune",
]

mods_kian = [
    "Magnetic Coating",
    "Universal System Crasher Mod",
    "Visual-Quantum Mod",
    "Aimbot",
    "High Mobility Retrofit",
]

systems_kian = [
    "BASTET-Class NHP",
    "SCHROEDINGER-Class NHP",
    "SHIVA-Class NHP",
    "INARI-Class NHP",
# Exoic
    "Flenser Macahuitl",
    "OTXO Injector",
    "Slayer's Cloak",
    "Luminary Drone",
    
    "Mertensian Litho-Code",
    "Motor-Sensor Dismemberment",
    "Ghastly Phantasmagoria",
    "Kaginawa Rappel",
    "Flight-Flight Module",
    "Panacea Package",
    "Liminal Mimesis",
    "Argus Module",
    "Eyes of the Sogenbi",
    "Visual System Override",
    "Temporal Suspension",
    "SUZU Emitter",
    "Armor of the Kasha",
    "YO Coolant Injector",
    "Circuit Killer",
    "Shikigami Firewall",
]

weapons_kian = [
    "Ferrofluid Dagger",
    "Butterfly Knife",
    "Particle Karambit",
    "Quick-Mod Knife",
    "Flare Saber",
    "Peryton Nexus",
    "Grasping Nexus",
    "Govardhana Projector",
    "Graverobber Odachi",
    "Kitsunebi Nexus",
    #"HC-Projektor",
]

PREFIXES = {
    "core_bonuses" : "cb",
    "frames" : "mf",
    "mods" : "wm",
    "systems" : "ms",
    "weapons" : "mw",
}

def build_for_domain(folder, domain_name, file_list):
    with open(os.path.join("templates", domain_name + ".yaml"), "r") as f:
        template = f.read()
    for fname in file_list:
        text = template
        if text[-1] != "\n": text += "\n"
        id_name = PREFIXES[domain_name] + "_" + re.sub(r"['\- ]", "_", fname.lower())
        text += f"id: {id_name}\n"
        if domain_name == "frames":
            text += f"license_id: {id_name}\n"

        path = os.path.join(folder, domain_name, fname.upper() + ".yaml")
        if os.path.exists(path):
            with open(path, "r+") as f:
                if f.readline() == "# IS AUTOGEN\n":
                    f.seek(0)
                    f.write(text)
                    f.truncate()
        else:
            with open(path, "w") as f:
                f.write(text)


def build_kierkegaard():
    build_for_domain("editable_content", "core_bonuses", core_bonus)
    build_for_domain("editable_content", "frames", frames)
    build_for_domain("editable_content", "mods", mods)
    build_for_domain("editable_content", "systems", systems)
    build_for_domain("editable_content", "weapons", weapons)


def build_kian_kierkegaard():
    build_for_domain("editable_content_Buona_Sera_ONRYO", "core_bonuses", core_bonus_kian)
    build_for_domain("editable_content_Buona_Sera_ONRYO", "frames", frames_kian)
    build_for_domain("editable_content_Buona_Sera_ONRYO", "mods", mods_kian)
    build_for_domain("editable_content_Buona_Sera_ONRYO", "systems", systems_kian)
    build_for_domain("editable_content_Buona_Sera_ONRYO", "weapons", weapons_kian)

if __name__ == "__main__":
    #build_kierkegaard()
    build_kian_kierkegaard()