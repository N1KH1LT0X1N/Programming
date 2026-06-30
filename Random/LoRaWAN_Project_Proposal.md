# LoRaWAN Sub-Surface Precision Network: Technical Proposal

## 1. Technical Details

### Background
**Review of work already done (Literature):**
Existing research highlights that soil behaves as a lossy dielectric, causing severe RF attenuation that increases exponentially with moisture content (Volumetric Water Content, VWC). Sub-GHz LoRa (865-867 MHz) offers better penetration than 2.4GHz, but reliable communication ranges are typically limited to 4–20 meters in wet soil (Al Moshi, MDPI 2024). Most current solutions rely on wired sensors that interfere with farm machinery or expensive TDR probes that lack wireless capability.

**Rationale for taking up the project:**
Precision agriculture requires accurate root-zone data, but surface sensors are vulnerable to damage from tractors, animals, and theft. A "zero-footprint" fully buried sensor network solves this durability crisis. Furthermore, Indian farmers need a cost-effective solution to monitor soil moisture at depth (30-100cm) to optimize irrigation in water-scarce regions.

**Relevance to State Priorities:**
This project directly aligns with state initiatives for **Water Conservation** (e.g., maximizing crop per drop in drought-prone areas) and **Soil Health Management**. By enabling precise monitoring of water and nutrient dynamics without obstructing field operations, it supports sustainable intensification of agriculture.

**Challenge & Constraints:**
*   **Physics of Propagation:** RF signal loss in wet soil can exceed 60dB, varying drastically with soil type (clay vs. sandy) and moisture levels.
*   **Power & Longevity:** Buried nodes must operate for years without battery replacement; retrieval is difficult.
*   **Deployment:** The antenna must be "soil-matched" to prevent detuning, and installation must avoid air gaps which distort readings.

### Description of Proposal
**Objectives of the project:**
1.  **Develop a Robust Underground-to-Aboveground (UG2AG) Link:** Design and characterize a sub-surface LoRaWAN communication node capable of transmitting data from 30cm+ depth to a surface gateway.
2.  **Create a "Root-Zone Intelligence" Node:** Integrate high-precision sensors to monitor VWC, temperature, and bulk conductivity (nutrient proxy) in real-time.
3.  **Demonstrate Scalability:** Validate the system in a field pilot (Month 4-8 plan) with an adaptive protocol that adjusts spreading factors (SF7→SF12) based on soil moisture conditions.

### Methodology
The project follows a phased "Lab-to-Land" approach:

1.  **Phase 1: Lab/Mud-Bucket Characterization (Weeks 1-4):**
    *   Test a single ESP32-LoRa node in controlled soil buckets at varying moisture levels (0% to saturation).
    *   Measure RSSI/SNR degradation to build attenuation curves for local soil types.
    *   **Innovation:** Tune the PCB antenna with a reflective ground plane to direct RF energy upwards, minimizing back-lobe loss.
    *   **Activation Mechanism:** Implement a **Magnetic Reed Switch** circuit to wake/sleep the buried node from the surface without digging, essential for sealed IP68 maintenance.

2.  **Phase 2: Depth Profiling & Calibration (Month 2-4):**
    *   Deploy nodes at 20, 50, and 100cm depths.
    *   **Risk Mitigation:** For the 100cm deep node, testing will confirm if direct UG2AG is viable; if attenuation is too high (>120dB), a "shallow repeater" architecture (node at 100cm wired to antenna at 20cm) will be evaluated.
    *   **Hybrid Sensing Strategy:** Use one **Industrial RS485 Modbus Sensor** (TDR-principle) as a "Ground Truth" reference to calibrate a network of lower-cost **Capacitive Probes**. This balances accuracy with affordability (Option B/A hybrid).

3.  **Phase 3: Field Pilot (Month 4-8):**
    *   Deploy a 5-node star network across 1-2 acres.
    *   Implement the **Moisture-Adaptive Protocol**: Nodes automatically increase transmit power and Spreading Factor (SF7→SF12) when soil gets wet (high attenuation), conserving battery during dry periods.
    *   **Localization:** Test the **Acoustic Homing** concept (piezo buzzer on node) to locate buried devices for retrieval.

### Problem Definition
"How to reliably transmit critical root-zone data (moisture, nutrients) from buried sensors to the surface in diverse soil conditions, overcoming extreme RF attenuation without using wired connections that hinder farm mechanization?"

### Architecture Diagram
*(Conceptual Description for Implementation)*

*   **Layer 1: The Buried Node (Sensing & TX)**
    *   **MCU:** ESP32-LoRa (Low power, deep sleep enabled)
    *   **Sensors:** Capacitive VWC Probe + DS18B20 Temp (Standard Nodes) / RS485 Modbus Sensor (Reference Node)
    *   **Control:** Magnetic Reed Switch (for non-intrusive activation/reset)
    *   **Antenna:** 868MHz PCB Antenna with Soil-Matching Network + Back Reflector
    *   **Power:** Li-SOCl2 Primary Battery (Multi-year lifespan)
    *   **Housing:** IP68 PVC Enclosure with Epoxy Potting

*   **Layer 2: The Surface Gateway (RX)**
    *   **Hardware:** SX1302 LoRa Concentrator on Raspberry Pi/ESP32
    *   **Position:** Pole-mounted (2-3m height) with High-Gain Omni Antenna (5-8dBi)
    *   **Power:** Solar Panel + Li-Ion Battery Backup

*   **Layer 3: Cloud & User Interface**
    *   **Network Server:** The Things Network (TTN)
    *   **Application:** Grafana Dashboard visualizing Soil Moisture Heatmaps & NPK trends

### Budget

| Name of Equipment | Cost (INR) |
| :--- | :--- |
| **ESP32-LoRa Dev Boards (x5 units)** | ₹7,500 |
| **Industrial RS485 Modbus Sensor (Reference Node)** | ₹4,500 |
| **Capacitive Soil Moisture Probes (x4 units)** | ₹1,200 |
| **Li-SOCl2 / Li-Ion Batteries + BMS (x5)** | ₹1,500 |
| **Gateway (RPi + LoRa HAT + Enclosure)** | ₹6,000 |
| **Enclosure (PVC/Epoxy) + Magnetic Switches** | ₹1,000 |
| **PCB Fabrication & Antenna Components** | ₹2,000 |
| **Total Estimated Budget** | **₹23,700** |

### Application
1.  **Smart Irrigation Scheduling:** Provides actionable data to automate drip irrigation, reducing water usage by 30-50% in water-stressed crops (e.g., pomegranate, grapes).
2.  **Precision Nutrient Management:** Monitoring soil conductivity trends helps prevent fertilizer leaching and ensures nutrients are available in the active root zone.
3.  **Research & Agronomy:** Enables universities and researchers to study root development and soil physics in-situ without disturbing the soil profile.
