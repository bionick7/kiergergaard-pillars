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
]

PREFIXES = {
    "core_bonus" : "cb",
    "frames" : "mf",
    "mods" : "wm",
    "systems" : "ms",
    "weapons" : "mw",
}

def build_for_domain(domain_name, file_list):
    with open(os.path.join("templates", domain_name + ".yaml"), "r") as f:
        template = f.read()
    for fname in file_list:
        text = template
        text += "\nid: " + PREFIXES[domain_name] + "_" + re.sub(r"['\- ]", "_", fname.lower())

        path = os.path.join("content_yaml", domain_name, fname + ".yaml")
        if os.path.exists(path):
            with open(path, "r+") as f:
                if f.readline() == "# IS AUTOGEN":
                    f.seek(0)
                    f.write(template)
                    f.truncate()
        else:
            with open(path, "w") as f:
                f.write(template)


if __name__ == "__main__":
    #build_for_domain("core_bonus", core_bonus)
    build_for_domain("frames", frames)
    #build_for_domain("mods", mods)
    build_for_domain("systems", systems)
    #build_for_domain("weapons", weapons)