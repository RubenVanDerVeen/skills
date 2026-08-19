# InvenTree naming: per-category formats
Name and description rules live in the [SKILL.md](../SKILL.md); this file holds the per-category detail.

## Fasteners

### Screws & Bolts

**Format:** `[Thread]x[Length] - [Head type] screw - [Drive]`

| Field | Examples |
|---|---|
| Thread × Length | `M3x8`, `M4x10`, `M5x16` |
| Head type | `Cap head`, `Countersunk head`, `Pan head`, `Button head` |
| Drive | `Hex`, `Phillips`, `Torx` |

**Name:** `M4x10 - Cap head screw - Hex`
**Description:** `M4 cap head hex socket screw, 10mm length.`

---

### Heat-Set Inserts

**Format:** `[Thread] Insert - Length=[X]mm ⌀=[Y]mm`

| Field | Examples |
|---|---|
| Thread | `M2`, `M3`, `M4` |
| Length | `4mm`, `5mm`, `6mm` |
| OD (⌀) | `3.5mm`, `4.2mm`, `6mm` |

**Name:** `M3 Insert - Length=4mm ⌀=4.2mm`
**Description:** `M3 hot-melt knurled brass heat-set insert for 3D-printed parts, 4mm length, 4.2mm outer diameter.`

---

## Bearings

**Format:** `[Part number] Ball Bearing ([Bore]×[OD]×[Width]mm)`

| Field | Examples |
|---|---|
| Part number | `6705-ZZ`, `18307-2RS`, `6803-2RS` |
| Suffix | `-ZZ` (steel shielded), `-2RS` (rubber sealed) |
| Dimensions | bore × OD × width in mm |

**Name:** `6705-ZZ Ball Bearing (25×32×4mm)`
**Description:** `Deep groove ball bearing, ZZ steel-shielded, 25mm bore × 32mm OD × 4mm width.`

**Name:** `18307-2RS Ball Bearing (18×30×7mm)`
**Description:** `Deep groove ball bearing, 2RS rubber-sealed, 18mm bore × 30mm OD × 7mm width.`

---

## Connectors

### Banana Jacks / Plugs

**Format:** `Banana Jack [Size] - [Male/Female] - [Color]`

**Name:** `Banana Jack 4mm - Female - Red`
**Name:** `Banana Jack 4mm - Female - Black`

---

### XT Connectors

**Format:** `[Series] Connector - [Male/Female]`

**Name:** `XT60 Connector - Male`
**Name:** `XT60 Connector - Female`

---

### JST Connectors

**Format:** `JST [Series] [Pitch]mm - [nP] - [Male/Female]`

| Field | Examples |
|---|---|
| Series | `XH`, `PH`, `GH`, `SH` |
| Pitch | `2.54mm`, `2.0mm`, `1.25mm` |
| Poles | `2P`, `3P`, `4P` |

**Name:** `JST XH 2.54mm - 2P - Male`
**Name:** `JST XH 2.54mm - 4P - Female`

---

### DC Barrel Jacks

**Format:** `DC Barrel Jack [OD]×[ID]mm - [Male/Female]`

**Name:** `DC Barrel Jack 5.5×2.1mm - Male`
**Name:** `DC Barrel Jack 5.5×2.1mm - Female`

---

### Pin Headers

**Format:** `Pin Header [Pitch]mm - [nP] - [Male/Female]`

**Name:** `Pin Header 2.54mm - 40P - Male`

---

## Switches

**Format:** `[Switch type] - [Poles/Throw/NO-NC] - [Voltage][/Amps]`
Additional details (waterproof, illuminated, latching, key-operated) go in the description.

| Field | Examples |
|---|---|
| Switch type | `Rocker Switch`, `Toggle Switch`, `Push Button 16mm`, `DIP Switch 5-Way`, `Key Rotary Switch 22mm` |
| Config | `SPST 1NO`, `SPDT 2NO`, `3P 6-Pin ON/OFF/ON` |
| Rating | `250V`, `12V 20A`, `250V 16A` |

**Name:** `Rocker Switch - SPST 1NO - 250V`
**Description:**
```
SPST rocker switch, 1NO contact, rated 250V.

Waterproof.
```

**Name:** `Push Button 16mm - 1NO 1NC - 12-24V`
**Description:**
```
Metal panel-mount push button, 16mm, 1NO 1NC contacts, rated 12–24V, black shell.

Waterproof.
Latching.
Illuminated (red LED).
```

**Name:** `DIP Switch - 5-Way - 2.54mm`
**Description:**
```
5-position DIP configuration switch, 2.54mm pitch.

PCB mount.
```

**Name:** `Key Rotary Switch 22mm - 3-Position 2NO 2NC`
**Description:**
```
Metal key-operated rotary switch, 22mm panel mount, 3-position, 2NO 2NC contacts.

Waterproof.
Latching.
```

---

## Dev Boards

**Format:** `Dev Board - [Controller + Chip] - [USB type]`

The controller section is a single segment: manufacturer/family followed by the chip (no dash between them).

| Field | Examples |
|---|---|
| Controller | `Arduino Nano ATmega328P`, `Arduino Mega ATmega2560`, `ESP32-WROOM-32`, `ESP32-S3-WROOM-1 N16R8`, `Pro Micro ATmega32U4`, `STM32 F411CEU6` |
| USB type | `USB-C`, `Micro-USB`, `USB-B` |

**Name:** `Dev Board - Arduino Nano ATmega328P - USB-C`
**Description:** `Arduino Nano-compatible development board, ATmega328P microcontroller, CH340 USB-C interface.`

**Name:** `Dev Board - ESP32-WROOM-32 - USB-C`
**Description:** `ESP32 dual-core development board, Wi-Fi + Bluetooth, 30-pin, USB-C interface.`

**Name:** `Dev Board - ESP32-S3-WROOM-1 N16R8 - USB-C`
**Description:** `ESP32-S3 development board, Wi-Fi + Bluetooth, 16MB flash, 8MB PSRAM, USB-C interface.`

**Name:** `Dev Board - Pro Micro ATmega32U4 - USB-C`
**Description:** `Arduino Leonardo-compatible development board, ATmega32U4 microcontroller, native USB, USB-C interface.`

**Name:** `Dev Board - STM32 F411CEU6 - USB-C`
**Description:** `STM32F411CEU6 ARM Cortex-M4 development board, 512KB flash, 128KB RAM, USB-C interface.`

---

## Power Modules

### Buck / Boost / Buck-Boost Converters

**Format:** `[Chip -] [Type] - [Input range] / [Max current or wattage]`

If the chip is unknown or unnamed, omit that section.

| Field | Examples |
|---|---|
| Chip (optional) | `LM2596`, `SC8701`, `XL6009` |
| Type | `Buck Converter`, `Boost Converter`, `Buck-Boost Converter` |
| Input range | `4.5-28V`, `8.5-50V`, `6-36V` |
| Output/rating | `3A`, `15A`, `400W` |

**Name:** `LM2596 - Buck Converter - 4.5-28V / 3A`
**Description:** `LM2596-based adjustable step-down converter module, 4.5–28V input, up to 3A output.`

**Name:** `Buck Converter - 4.5-28V / 5A` *(no chip)*
**Description:** `Synchronous adjustable step-down converter module, 4.5–28V input, up to 5A output.`

**Name:** `SC8701 - Buck-Boost Converter - 150W / 12A`
**Description:** `SC8701-based synchronous buck-boost converter module, wide input range, 150W, up to 12A.`

---

### BMS (Battery Management Systems)

**Format:** `[Chip -] [nS] BMS - [Max current]`

Balance, protection features, and cell chemistry go in the description.

**Name:** `2S BMS - 20A`
**Description:** `2S lithium battery management system, 7.4V nominal, 20A continuous discharge protection.`

Features like cell balancing, overcharge, overdischarge, and short-circuit protection go as feature flags:
```
2S lithium battery management system, 7.4V nominal, 20A continuous discharge protection.

Cell balancing.
Overcharge protection.
Overdischarge protection.
Short-circuit protection.
```

---

### Battery Chargers

**Format:** `[Chip -] [nS] [Chemistry] Charger - [Max current] - [USB type]`

**Name:** `IP2312 - 1S LiPo Charger - 3A - USB-C`
**Description:** `IP2312-based single-cell LiPo charger module, CC/CV charging, 3A max, USB-C input.`

**Name:** `1S LiPo Charger - 3A - USB-C` *(no chip)*
**Description:** `Single-cell LiPo charger module, CC/CV charging, 3A max, USB-C input.`

**Name:** `IP2368 - 4S Power Bank Module - 100W - USB-C`
**Description:** `IP2368-based bidirectional buck-boost fast-charge controller for 4S Li-Ion power banks, 100W, USB-C.`

---

## Motors

**Format:** `[Motor type] - [Model/Voltage range] - [KV/RPM]`

| Field | Examples |
|---|---|
| Motor type | `BLDC Motor`, `DC Motor`, `Stepper Motor`, `Servo Motor` |
| Model/range | `A2212`, `6210`, `3-12V` |
| Speed | `200KV`, `2450KV`, `34-136RPM` |

**Name:** `BLDC Motor - 6210 - 200KV`
**Description:** `6210-frame brushless outrunner motor, 200KV, high torque for industrial or agricultural use.`

**Name:** `BLDC Motor - A2212 - 2450KV`
**Description:** `A2212-frame brushless outrunner motor, 2450KV, for RC aircraft and FPV applications.`

**Name:** `DC Motor - 3-12V - 34-136RPM`
**Description:** `All-metal worm gear DC motor, 3–12V input, 34–136RPM output, right-angle shaft.`

---

## Displays

**Format:** `[Type] Display - [Size] - [Interface] - [Driver] - [Resolution]`

Resolution is optional for displays where it's implied by the driver.

| Field | Examples |
|---|---|
| Type | `OLED`, `TFT`, `LCD`, `E-Ink` |
| Size | `0.91in`, `2.8in`, `4.0in` |
| Interface | `I2C`, `SPI`, `Parallel` |
| Driver | `SSD1306`, `ST7789V`, `ILI9341` |
| Resolution (optional) | `128×32`, `240×320` |

**Name:** `OLED Display - 0.91in - I2C - SSD1306`
**Description:** `0.91-inch OLED display module, I2C interface, SSD1306 driver, 128×32 resolution, 3.3–5V.`

**Name:** `TFT Display - 2.8in - SPI - ST7789V - 240×320`
**Description:** `2.8-inch colour TFT display module, SPI interface, ST7789V driver, 240×320 resolution.`

**Name:** `TFT Display - 2.8in - SPI - ST7789V - 240×320` *(with touch)*
**Description:**
```
2.8-inch colour TFT display module, SPI interface, ST7789V driver, 240×320 resolution.

Resistive touchscreen.
```

---

## Tools

**Format:** `[Type] - [Brand] [Model]`

If the tool has no brand or model, omit that section.

| Field | Examples |
|---|---|
| Type | `Soldering Iron`, `Hot Air Station`, `Multimeter`, `Oscilloscope`, `LCR Meter`, `Power Supply`, `Drill`, `Rotary Tool` |
| Brand + Model | `FNIRSI HS-02`, `Hakko FX-888D`, `Rigol DS1054Z` |

**Name:** `Soldering Iron - FNIRSI HS-02`
**Description:** `FNIRSI HS-02 adjustable temperature soldering iron, DC 20V input, 100–450°C, compatible with TS-B2 tips.`

**Name:** `LCR Meter - FNIRSI LCR-ST2`
**Description:** `FNIRSI LCR-ST2 2-in-1 digital tweezer LCR/ESR meter for SMD component testing, measures L, C, R and ESR.`

**Name:** `Desoldering Pump`
**Description:** `Aluminium spring-loaded desoldering pump for removing molten solder from through-hole components.`

Categories:
- **Tools/Soldering & Rework** - soldering irons, desoldering pumps, hot air stations, tip cleaners
- **Tools/Measurement & Testing** - multimeters, oscilloscopes, LCR meters, bench power supplies
- **Tools/Hand Tools** - pliers, cutters, screwdrivers, tweezers, blowers
- **Tools/Power Tools** - drills, rotary tools, electric screwdrivers
