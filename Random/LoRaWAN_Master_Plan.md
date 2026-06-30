# LoRaWAN Sub-Surface Precision Network: Master Project Plan

## Executive Summary
This document outlines a phased execution strategy for developing a "Root-Zone Intelligence" system. It combines a rapid, low-cost "MVP Phase" to validate core physics with a rigorous "Pilot Phase" to deliver a scalable precision agriculture solution. This approach de-risks the technical challenges (RF attenuation in soil) while ensuring commercial and scientific impact.

---

## Phase 1: The "Proof of Physics" MVP (Weeks 1-2)
**Goal:** Demonstrate wireless transmission from 30cm underground using <₹3,000 hardware.
**Deliverable:** A functional "Buried Probe" and "Handheld Receiver" demo.

### 1.1 Objectives
*   Validate that LoRa (868MHz) can penetrate 30cm of local soil (Red/Black Cotton).
*   Test the "Wire Antenna" vs. "Coil Antenna" performance difference.
*   Prove the "Sleep-Wake-Sense-Tx" power cycle works on a single 18650 battery.

### 1.2 Hardware BOM (The "Shoestring" Kit)
*   **Nodes:** 2x ESP32-LoRa (SX1276) Modules **(MUST be 865-867 MHz for India compliance)**
*   **Sensor:** 1x Capacitive Soil Moisture Sensor v1.2 (Waterproofed)
*   **Power:** 1x 18650 Battery + TP4056 Charger
*   **Mechanical:** 4-inch PVC Pipe + End Caps

### 1.3 Key Activities
1.  **Assembly:** Solder wire antennas (8.6cm). Waterproof sensor electronics with hot glue.
2.  **Coding:** Flash "Point-to-Point" firmware (Sender/Receiver) using `LoRa.h`.
3.  **Field Test:** Bury node. Measure RSSI at 0m, 5m, 10m, 20m.

---

## Phase 1.5: The "Single-Channel" Bridge (Weeks 3-4)
**Goal:** Connect the MVP node to the Internet without buying a ₹6,000 Gateway.
**Strategy:** Repurpose the MVP "Receiver" node as a **Single-Channel LoRaWAN Gateway** (ESP32-Dual-Chan-GW firmware).
**Outcome:** Push live data to The Things Network (TTN) for free. This validates the "Cloud" part of the architecture using only MVP hardware.

---

## Phase 2: The "Precision Agriculture" Pilot (Months 2-6)
**Goal:** Deploy a calibrated, 5-node star network with a Gateway and Cloud Dashboard.
**Deliverable:** A field-deployed system generating "Soil Moisture Heatmaps" for irrigation.

### 2.1 Objectives
*   **Depth:** Push transmission to 50-100cm (Root zone of orchards).
*   **Accuracy:** Calibrate capacitive sensors against an **Industrial RS485 Reference Node**.
*   **Longevity:** Implement "Moisture-Adaptive Protocol" (SF7→SF12) to survive monsoon seasons.

### 2.2 Hardware Upgrade (The "Pro" Kit)
*   **Network:** 5x Custom Nodes (PCB Antenna + Ground Plane Reflector).
*   **Gateway:** Raspberry Pi + SX1302 Concentrator (Solar Powered).
*   **Reference:** 1x Industrial RS485 Modbus Sensor (TDR-principle).
*   **Maintenance:** Magnetic Reed Switches for non-intrusive reset.

### 2.3 Key Activities
1.  **Lab Characterization:** Create "VWC vs. Attenuation" curves for the site's specific soil.
2.  **Deployment:** Install 5 nodes in a star topology (1 Reference + 4 Standard).
3.  **Data Platform:** Set up The Things Network (TTN) -> Grafana Dashboard.

---

## Comparison of Phases

| Feature | Phase 1 (MVP) | Phase 2 (Pilot) |
| :--- | :--- | :--- |
| **Objective** | Proof of Concept | Field Validation |
| **Connectivity** | Point-to-Point (No Internet) | LoRaWAN Gateway (Cloud) |
| **Range** | ~20-50m (Line of Sight) | ~200-500m (with Gateway) |
| **Depth** | 30cm (Shallow) | 20cm, 50cm, 100cm (Deep) |
| **Sensor Accuracy** | Relative (Wet vs. Dry) | Calibrated (% VWC) |
| **Budget** | ~₹3,050 | ~₹23,700 |
| **Timeframe** | 2 Weeks | 4-6 Months |

---

## Immediate Next Steps
1.  **Procure Phase 1 Materials:** Buy 2x ESP32-LoRa boards and 1x Capacitive Sensor immediately.
2.  **Build the MVP:** Assemble the "PVC Pipe Node" this weekend.
3.  **Field Test:** Run the "Bucket Test" to verify signal penetration before investing in Phase 2 components.
