
// ==================================  DATA  ===================================

#let frames = json("frames.json").map(d => d + (file_source: "frames"))
#let weapons = json("weapons.json").map(d => d + (file_source: "weapons"))
#let systems = json("systems.json").map(d => d + (file_source: "systems"))
#let mods = json("mods.json").map(d => d + (file_source: "weapon_mods"))
#let manufacturers = json("manufacturers.json").map(d => d + (file_source: "manufacturers"))

#let equipment = weapons + systems + mods

#let LIGHT_RED = rgb("#f5253b")
#let DEFAULT_RED = rgb("c22026")
#let DARK_RED = rgb("#4e0000")

#let STAT_DISPLAY = (
  size: "Size",
  structure: "Structure",
  stress: "Stress",
  armor: "Armor",
  edef: "E-Defense",
  evasion: "Evasion",
  heatcap: "Heat",
  repcap: "Repair",
  save: "Save Target",
  sensor_range: "Sensors",
  speed: "Speed",
  hp: "HP",
  tech_attack: "Tech Attack",
  sp: "System Points",
)

#let MOUNT_NAMES = (
  Aux: "AUX MOUNT",
  Main: "MAIN MOUNT",
  Flex: "FLEX MOUNT",
  Heavy: "HEAVY MOUNT",
  "Aux/Aux": "AUX/AUX",
  "Main/Aux": "MAIN/AUX",
)

#let TAGS = (
  
)

#let COLOR_PALETTE = (
  weapon: (rgb("#000000"), rgb("#f2f2f2")),
  system: (rgb("#68bd45"), rgb("#e1f2da")),
  mod: (rgb("#68bd45"), rgb("#e1f2da")),
  tech: (rgb("#7e2477"), rgb("#f2e9f1")),
  reaction: (rgb("#0b7675"), rgb("#e7f1f1")),
  ai: (rgb("#d60000"), rgb("#fde8e7")),
  protocol: (rgb("#d75000"), rgb("#fceee5")),
  traits: (DEFAULT_RED, rgb("#f9e9e9"))
)

// ==================================  STYLING  ===================================

#show heading.where(level: 1): it => (
  align(center, text(
    size: 24pt,
    fill: DEFAULT_RED, 
    strong(it)
  ))
)
#set text(
  font: "DM Sans",
  overhang: true
)
#set par(
  leading: 4pt,
)
#set page(
  numbering: "[1]",
  number-align: right,
  margin: (left: 3em, right: 3em, bottom: 5em),
  columns: 1
)

// ==================================  UTILITY  ===================================

#let unescape_html(inp) = {
  // TODO: properly handle lists etc
  inp.replace("<br>", "\n").replace(regex("</?[a-z]+>"), "")
}

#let box_display(name, header1, header2, body, color_tuple) = {
  box(
  stack(dir: ttb,
    rect(
      text(fill: white, 
        heading(level: 4, upper(name)) + 
        if header1.len() > 0 {header1.join(h(10pt))} + 
        if header2.len() > 0 {linebreak() + header2.join(h(10pt))}
      ),
      width: 100%, stroke: 0pt, fill: color_tuple.first()
    ),
    rect(body, width: 100%, stroke: 0pt, fill: color_tuple.last())
  ))
}

#let format_tags(tags) = {
  tags.map(x => 
    if "val" in x {x.id.trim("tg_") + "(" + str(x.val) + ")"}
    else {x.id.trim("tg_")}
  )
}

#let format_range(range_data) = {
  range_data.type + h(5pt) + [#range_data.val] + h(8pt)
}

#let format_dmg(dmg_data) = {
  [#dmg_data.val] + h(5pt) + dmg_data.type + h(8pt)
}

// ==================================  EQUIPMENT  ===================================

#let display_reaction(reaction_data) = {
  box(
  stack(dir: ttb,
    rect(
      width: 100%, stroke: 0pt, fill: COLOR_PALETTE.reaction.first(),
      text(fill: white, heading(level: 3, reaction_data.name) + [Reaction] + h(10pt) + reaction_data.frequency)
    ),
    rect(
      width: 100%, stroke: 0pt, fill: white,
      text(fill: black, [*Trigger:* ] + reaction_data.trigger)
    ),
    rect(
      width: 100%, stroke: 0pt, fill: COLOR_PALETTE.reaction.last(),
      text(fill: black, [*Effect:* ] + reaction_data.effect)
    )
  ))
}

#let display_weapon(weapon_data) = {
  let body = unescape_html(weapon_data.at("effect_print", default: weapon_data.at("effect", default:"")))
  if weapon_data.at("description", default:"") != "" {
    body = body + line(length: 100%, stroke: (dash: "densely-dashed")) + emph(unescape_html(weapon_data.description))
  }
  let header1 = (weapon_data.mount, weapon_data.type, ..format_tags(weapon_data.at("tags", default:())))
  if "sp" in weapon_data {
    header1 = (str(weapon_data.sp) + " SP", ..header1)
  }
  if "on_crit" in weapon_data {
    body = [*On Critical hit:* ] + weapon_data.on_crit + linebreak() + body
  }
  if "on_hit" in weapon_data {
    body = [*On Hit:* ] + weapon_data.on_hit + linebreak() + body
  }
  if "on_attack" in weapon_data {
    body = [*On Attack:* ] + weapon_data.on_attack + linebreak() + body
  }
  let header2 = (
    weapon_data.at("range", default: ()).map(format_range).join(), 
    weapon_data.at("damage", default: ()).map(format_dmg).join()
  )
  box_display(weapon_data.name, header1, header2, body, COLOR_PALETTE.weapon)
}

#let display_tech_system(system_data) = {
  let body = unescape_html(system_data.at("effect_print", default: system_data.at("effect", default:"No effect")))
  for action in system_data.at("actions", default:()) {
    body += rect(
      stroke: (
        "top": 2pt + COLOR_PALETTE.tech.first(),
        "bottom": 2pt + COLOR_PALETTE.tech.first(),
        "left": 0pt,
        "right": 0pt
      ),
      fill: white,
      outset: 5pt,
      width: 100%
    )[*#action.name*: #action.detail]
  }
  if system_data.at("description", default:"") != "" {
    body = body + line(length: 100%, stroke: (dash: "densely-dashed")) + emph(unescape_html( system_data.description))
  }
  let header = (str(system_data.sp) + " SP", ..format_tags(system_data.tags))
  box_display(system_data.name, header, (), body, COLOR_PALETTE.tech)
}

#let display_nontech_system(system_data) = {
  let body = unescape_html(system_data.at("effect_print", default: system_data.at("effect", default:"No effect")))
  let colors = COLOR_PALETTE.system
  if system_data.at("actions", default: ()).any(x => x.activation == "Protocol") {
    colors = COLOR_PALETTE.protocol
  }
  if system_data.type == "AI" {
    colors = COLOR_PALETTE.ai
  }
  if system_data.at("description", default:"") != "" {
    body = body + line(length: 100%, stroke: (dash: "densely-dashed")) + emph(unescape_html( system_data.description))
  }
  let header = (str(system_data.sp) + " SP", ..format_tags(system_data.tags))
  box_display(system_data.name, header, (), body, colors)
}

#let display_system(system_data) = {
  if system_data.type == "Tech" {
    display_tech_system(system_data)
  } else {
    display_nontech_system(system_data)
  }
}

#let display_weapon_mod(mod_data) = {
  let body = unescape_html(mod_data.at("effect_print", default: mod_data.at("effect", default:"No effect")))
  if mod_data.at("description", default:"") != "" {
    body = body + line(length: 100%, stroke: (dash: "densely-dashed")) + unescape_html( mod_data.description)
  }
  box_display(mod_data.name, (), (), body, COLOR_PALETTE.mod)
}

// ==================================  FRAME  ===================================

#let display_stats(stat_dict) = {
  let disp(stat_id) = {
    STAT_DISPLAY.at(stat_id) + " :" + h(5pt) + str(stat_dict.at(stat_id))
  }
  let stat_heading(name) = text(fill: DEFAULT_RED, strong(name))
  heading(level: 2)[STATS]
  //grid(columns: 2, ..STAT_DISPLAY.pairs().map(
  //p => p.last() + v(-7pt) + str(stat_dict.at(p.first()))
  //))
  grid(columns: 2, row-gutter: 8pt, column-gutter: 15pt,
  disp("size"), disp("save"),
  disp("armor"), disp("sensor_range"),
  stat_heading("HULL"), stat_heading("SYSTEMS"),
  h(15pt) + disp("hp"), h(15pt) + disp("edef"),
  h(15pt) + disp("repcap"), h(15pt) + disp("tech_attack"),
  stat_heading("AGILITY"), h(15pt) + disp("sp"),
  h(15pt) + disp("evasion"), stat_heading("ENGINEERING"),
  h(15pt) + disp("speed"), h(15pt) + disp("heatcap"),
  )
  linebreak()
}

#let display_traits(trait_list) = {
  heading(level: 2)[TRAITS]
  for trait in trait_list {
    box_display(trait.name, (), (), trait.description, COLOR_PALETTE.traits)
  }
}

#let display_mounts(mount_list) = {
  heading(level: 2)[MOUNTS]
  grid(columns: (33%, 33%, 33%), column-gutter: 10pt, ..mount_list.map(
    x => box(
      fill: DEFAULT_RED, width: 100%, inset: 10pt,
      align(center, text(fill: white, size: 15pt, strong(MOUNT_NAMES.at(x))))
    )
  ))
}

#let display_core_system(core) = {
  heading(level: 2)[CORE SYSTEM]
  heading(level: 3, core.name)
  par(unescape_html(core.at("description", default:"")), justify: true)
  for integrated_id in core.at("integrated", default:()){
    display_weapon(weapons.find(d => d.id == integrated_id))
  }
  let colors = COLOR_PALETTE.system
  if core.activation == "Protocol" { colors = COLOR_PALETTE.protocol }
  box_display(core.active_name, ("Active (1 CP)", core.activation), (), par(unescape_html(core.active_effect)), colors)
  for action in core.at("actions", default:()) {
    if action.activation == "Reaction" {
      display_reaction(action)
    }
  }
}

#let display_frame(frame_data) = {
  align(center, stack(dir: ttb, 
    text(font: "Barlow", fill: DEFAULT_RED, weight: "extralight", size: 24pt, frame_data.source) + v(1em),
    text(fill: DEFAULT_RED, size: 24pt, frame_data.name) + v(1em),
    text(fill: DEFAULT_RED, frame_data.mechtype.join("/")),
  ))
  par(unescape_html(frame_data.description), justify: true)
  rect(
    stroke: DEFAULT_RED + 2pt,
    columns(2,
      display_stats(frame_data.stats) + 
      display_traits(frame_data.traits) + 
      display_mounts(frame_data.mounts) +
      colbreak() +
      display_core_system(frame_data.core_system)
    )
  )
}

#let display_license(frame_name, license_id) = {
  let license_counter = counter("license")
  counter("license").update(1)
  let license_box(color, content) = {
    set text(fill: white, size: 12pt)
    box(fill: color, inset: 5pt, width: 100%, [License] + license_counter.display(" I: ") + content.map(
      x => x.name
    ).join([, ])) + linebreak()
    license_counter.step()
  }
  let lls = range(1, 4).map(x => equipment.filter(d => d.at("license_id", default:"") == license_id and d.at("license_level", default:-999) == x))
  // Print licens structure
  columns(2, 
  for i in range(3){
    license_box((LIGHT_RED, DEFAULT_RED, DARK_RED).at(i), lls.at(i))
    for equipment in lls.at(i){
      if equipment.file_source == "weapons" { display_weapon(equipment) }
      if equipment.file_source == "systems" { display_system(equipment) }
      if equipment.file_source == "weapon_mods" { display_weapon_mod(equipment) }
      for action in equipment.at("actions", default:()) {
        if action.activation == "Reaction" {
          display_reaction(action)
        }
      }
    }
  })
}

#let display_manufacturer(manufacturer) = {
  [= #manufacturer.name]
  emph(unescape_html(manufacturer.quote))
  linebreak()
  unescape_html(manufacturer.description)
}

// ==================================  FILE  ===================================

#par(leading: 8pt, outline(depth: 1))
#for manufacturer in manufacturers {
  pagebreak()
  display_manufacturer(manufacturer)
  for frame_data in frames.filter(x => x.source == manufacturer.id) {
    pagebreak()
    display_frame(frame_data)
    display_license(frame_data.name, frame_data.license_id)
  }
}