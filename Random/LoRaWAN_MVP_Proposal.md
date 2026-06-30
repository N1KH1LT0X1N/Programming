# Low-Budget MVP Proposal: Frugal Sub-Surface Sensor

## 1. Technical Details

### Background
**Rationale for Frugal Innovation:**
Many small-scale Indian farmers operate on razor-thin margins and cannot afford complex IoT systems costing ₹20,000+. To democratize precision agriculture, we need a "Jugaad" approach: proving that reliable sub-surface sensing is possible with off-the-shelf components for under ₹2,000 per node.

**Challenge & Constraints:**
*   **Cost:** The BOM must stay below ₹3,000 for a functional pair (Transmitter + Receiver).
*   **Simplicity:** No custom PCBs or complex gateways. The system must work "out of the box" with standard hobbyist modules.
*   **Physics:** Overcoming soil attenuation using only wire antennas and basic LoRa modulation.

### Description of Proposal
**Objectives of the MVP:**
1.  **Build a Single-Node "Probe":** Assemble a robust, battery-powered soil moisture sensor using ESP32-LoRa and capacitive sensing.
2.  **Demonstrate Wireless Link:** Successfully transmit data from 30cm depth (standard root zone) to a handheld receiver at least 10-50m away.
3.  **Visualize Attenuation:** Display real-time signal strength (RSSI) on the receiver to educate users about soil signal loss.

### Methodology (The "Rapid" Plan)
**Week 1: Assembly & Coding**
*   **Hardware:** Solder the Capacitive Sensor v1.2 to the ESP32-LoRa module.
*   **Antenna:** Solder a simple **8.6cm Wire Antenna** (1/4 wave for 868MHz) to replace the stock coil, ensuring decent range.
*   **Waterproofing:** Apply **Nail Polish or Hot Glue** to the exposed electronics on the sensor top to prevent corrosion.
*   **Enclosure:** Seal the electronics inside a 4-inch PVC pipe with end caps.
*   **Code:** Write a simple "Deep Sleep (1 hour) -> Wake -> Read Sensor -> Send LoRa Packet -> Sleep" loop.

**Week 2: Testing & Demo**
*   **The Bucket Test:** Bury the node in a bucket of dry soil. Measure RSSI on the handheld receiver. Gradually add water.
*   **The Field Range Test:** Bury the node at 1ft depth in a garden/field. Walk away with the receiver to find the maximum transmission range.

### Problem Definition
"Can we build a sub-surface soil sensor for under ₹1,500 that reliably signals 'Needs Water' to a farmer's handheld device without internet or expensive gateways?"

### Architecture Diagram
*(Simplified Point-to-Point System)*

*   **Unit 1: The Buried Transmitter**
    *   **MCU:** TTGO LoRa32 / ESP32-LoRa Module (SX1276 - 868MHz for India)
    *   **Sensor:** Capacitive Soil Moisture Sensor v1.2 (Waterproofed)
    *   **Antenna:** 8.6cm Wire Monopole (Soldered)
    *   **Power:** 1x 18650 Li-Ion Battery + TP4056 Charger Module
    *   **Power Tip:** Remove the status LED on the TP4056 to save battery.
    *   **Housing:** 4-inch PVC Pipe Section with End Caps

*   **Unit 2: The Handheld Receiver**
    *   **MCU:** TTGO LoRa32 (with built-in OLED Display)
    *   **Power:** USB Power Bank (Phone Charger)
    *   **Function:** Receives packets and displays: "Moisture: 45%", "Signal: -112dBm"
    *   **Alert:** Blinks an LED if moisture < 30% (Dry)

### Budget (The "Shoestring" Version)

| Name of Equipment | Cost (INR) | Notes |
| :--- | :--- | :--- |
| **TTGO LoRa32 / ESP32-LoRa (SX1276)** | ₹2,400 | **Must be 868MHz** |
| **Capacitive Soil Sensor v1.2 (x1)** | ₹150 | Standard analog probe |
| **18650 Li-Ion Battery + TP4056 Charger (x1)** | ₹200 | Remove LED to save power |
| **PVC Pipe (4-inch) & End Caps** | ₹200 | Local hardware store |
| **Jumper Wires & Consumables** | ₹100 | Solder, glue, tape |
| **Total MVP Budget** | **~₹3,050** | Extremely affordable |

### Application
1.  **Home Garden/Nursery Monitor:** Simple alert system for potted plants or small vegetable patches.
2.  **Educational Demonstration:** A low-cost tool for students to visualize RF physics (signal attenuation) in soil.
