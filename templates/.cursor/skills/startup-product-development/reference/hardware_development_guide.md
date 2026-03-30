# Hardware Development Guide

> **From concept to manufacturing for physical products**

## Development Phases

### Phase 1: Concept (Weeks 1-2)

**Deliverables**:
- Hand sketches of product
- Block diagram of system architecture
- Bill of Materials (BOM) estimate
- Feature requirements
- Target cost per unit

**Activities**:
- Brainstorm form factor
- Research components (sensors, MCU, connectivity)
- Estimate power requirements
- Identify regulatory requirements

### Phase 2: Breadboard Prototype (Weeks 3-8)

**Goal**: Prove core functionality works

**Tools**:
- Breadboard
- Jumper wires
- Development boards (Arduino, ESP32, Raspberry Pi)
- Power supply
- Multimeter/oscilloscope

**Deliverables**:
- Working breadboard prototype
- Firmware demonstrating core features
- Power consumption measurements
- Component selection finalized

**Common Issues**:
- Wiring mistakes (use wire colors consistently)
- Power supply noise (add decoupling capacitors)
- Ground loops (single ground point)

### Phase 3: PCB Design (Weeks 9-16)

**Tools**: KiCad (free), Eagle, Altium Designer

**Steps**:
1. **Schematic Design**: Component connections
2. **PCB Layout**: Physical component placement
3. **Design Rule Check (DRC)**: Verify no errors
4. **Generate Gerber Files**: Manufacturing files
5. **Order PCBs**: JLCPCB, PCBWay, OSH Park

**PCB Design Checklist**:
- [ ] Power traces wide enough (1mm for 1A)
- [ ] Decoupling capacitors near ICs
- [ ] Ground plane on bottom layer
- [ ] Clearance rules met (6mil minimum for cheap boards)
- [ ] Silkscreen labels clear and useful
- [ ] Test points for debugging
- [ ] Mounting holes positioned correctly

**Turnaround**: 1-2 weeks from order to delivery

### Phase 4: PCB Bring-Up (Weeks 17-20)

**Process**:
1. Visual inspection for shorts/defects
2. Power test (measure voltages before connecting battery)
3. Program firmware
4. Test each subsystem individually
5. Debug issues (expect rev 2 or 3)

**Common Rev 1 Issues**:
- Swapped pins
- Missing pull-up/pull-down resistors
- Wrong footprints (check datasheets!)
- Antenna placement issues (WiFi/BLE)

### Phase 5: Enclosure Design (Weeks 18-24)

**Tools**: Fusion 360 (free for startups), SolidWorks, OnShape

**Considerations**:
- Material: ABS, PLA (3D printed), injection molded
- Assembly: Snap fit, screws, glue
- Cutouts: Buttons, ports, LEDs, sensors
- Waterproofing (IP rating if outdoor use)

**Prototyping**:
- 3D print enclosures (FDM: $200-500, SLA: $1K-3K)
- Iterate on fit and finish
- Test drop resistance

**Injection Molding** (for production):
- Tooling cost: $3K-20K per part
- Unit cost: $0.50-5 per part
- MOQ: 500-1000 units

### Phase 6: Pre-Production (Weeks 25-32)

**Goal**: Validate design for mass manufacturing

**Activities**:
- Design for Manufacturing (DFM) review with CM
- Order pilot run (50-100 units)
- Functional testing of all units
- Firmware bug fixes
- Regulatory testing (FCC, CE)

**Contract Manufacturer (CM) Selection**:
- Get quotes from 3-5 CMs
- Check references
- Visit facility if possible
- Negotiate pricing and terms

### Phase 7: Certifications (Weeks 28-40)

**FCC (US)**:
- Required for: RF devices (WiFi, Bluetooth, cellular)
- Cost: $3K-10K
- Time: 4-8 weeks
- Process: Submit to test lab, fix issues, get cert

**CE (Europe)**:
- Required for: All electronics sold in EU
- Cost: $2K-8K
- Self-certification possible for some categories

**UL (Safety)**:
- Required for: Products plugged into wall power
- Cost: $5K-15K
- Time: 8-12 weeks

**IP Rating** (Water/Dust Resistance):
- IP65: Dust-tight, water spray resistant
- IP67: Dust-tight, immersion up to 1m
- IP68: Dust-tight, prolonged immersion
- Cost: $2K-5K for testing

### Phase 8: Manufacturing (Weeks 36+)

**First Production Run**:
- Start small: 500-1000 units
- Quality control: Inspect sample from each batch
- Expect 1-3% defect rate initially

**Scaling Production**:
- 1K-10K units: Small batch manufacturing
- 10K-100K units: Dedicated production line
- 100K+ units: Multiple CMs, negotiate pricing

**Lead Times**:
- PCB assembly: 2-4 weeks
- Enclosure molding: 4-8 weeks
- Final assembly: 1-2 weeks
- Shipping: 2-6 weeks (air/sea)

## BOM Management

### Component Selection

**Criteria**:
- Availability (not end-of-life)
- Multiple suppliers (avoid single-source)
- Cost at volume (1K, 10K, 100K pricing)
- Package size (SMD components for production)

**Component Categories**:
- **Microcontroller**: ESP32 ($2-5), STM32 ($1-3)
- **Sensors**: BME280 ($3), MPU6050 ($2)
- **Connectivity**: WiFi module ($5-10), Bluetooth ($3-8)
- **Power Management**: LDO regulators ($0.50), LiPo charger ($1-2)
- **Passives**: Resistors, capacitors ($0.01-0.10 each)

### Cost Breakdown

**Example: Smart Home Sensor**

| Component | Unit Cost (1K qty) | % of BOM |
|-----------|-------------------|----------|
| ESP32-C3 | $2.50 | 25% |
| Sensors (temp, humidity, motion) | $3.00 | 30% |
| PCB (4-layer) | $1.50 | 15% |
| Enclosure (injection molded) | $1.00 | 10% |
| Battery (LiPo 1000mAh) | $1.50 | 15% |
| Passives (R, C, L) | $0.50 | 5% |
| **Total BOM** | **$10.00** | **100%** |

**Retail Pricing**: BOM × 4-5 = $40-50 retail

## Firmware Development

### Embedded Programming

**Languages**: C, C++, MicroPython (for prototyping)

**Development Boards**:
- Arduino: easiest for beginners
- ESP32: WiFi/BLE, powerful
- STM32: production-grade, ARM Cortex-M

**Development Flow**:
1. Write code in IDE (Arduino IDE, PlatformIO, STM32Cube)
2. Compile firmware
3. Flash to device via USB/JTAG
4. Test and debug (serial monitor, LEDs, oscilloscope)
5. Iterate

### OTA Updates

**Over-The-Air firmware updates**:
- Critical for fixing bugs post-launch
- ESP32 has built-in OTA support
- Implement secure updates (signed firmware)

### Power Optimization

**Techniques**:
- Sleep modes (deep sleep < 10µA on ESP32)
- Wake on interrupt (motion sensor, timer)
- Reduce WiFi transmit power
- Use BLE instead of WiFi when possible

**Battery Life Calculation**:
```
Battery capacity: 1000mAh
Average current: 10mA
Battery life = 1000mAh / 10mA = 100 hours ≈ 4 days

With sleep mode (1mA average):
Battery life = 1000mAh / 1mA = 1000 hours ≈ 42 days
```

## Supply Chain

### Component Sourcing

**Distributors**:
- Digi-Key (US, huge selection, fast shipping)
- Mouser (US, similar to Digi-Key)
- LCSC (China, cheap, long lead times)
- Alibaba (bulk orders, negotiate pricing)

**Lead Time Management**:
- Order long-lead components early (6-12 weeks)
- Keep safety stock for critical parts
- Have backup suppliers

**COVID/Chip Shortage Lessons**:
- Diversify component sources
- Design with common components
- Avoid single-source parts

## Quality Control

### Incoming QC

**Inspect components on arrival**:
- Visual inspection for damage
- Verify part numbers match order
- Sample test critical components

### Production QC

**100% Functional Testing**:
- Power-on test
- WiFi connectivity test
- Sensor readings verification
- Button/LED functionality
- Battery charging test

**Sample Testing** (from each batch):
- Environmental testing (temperature, humidity)
- Drop test
- Long-term reliability test

### Field Failures

**RMA Process**:
- Track defect rates
- Identify common failure modes
- Implement fixes in next production run
- Offer warranty replacements

**Target Metrics**:
- < 2% defect rate in production
- < 5% RMA rate in first year

## Regulatory Strategy

### Certification Timeline

**Plan early** (add 6 months to timeline for certs):
- FCC/CE required before selling in US/EU
- UL required for wall-powered devices
- Budget $10K-30K for all certifications

### Test Lab Selection

**Accredited Labs**:
- Intertek
- UL
- TÜV
- Bureau Veritas

**Process**:
1. Submit samples and documentation
2. Lab tests for compliance
3. Address any failures
4. Retest
5. Receive certification

## Manufacturing Partners

### Contract Manufacturers (CM)

**Domestic (US)**:
- Pros: Faster communication, smaller MOQs, easier QC
- Cons: 3-5x cost vs China
- Use for: Pilot runs, low volume (<5K units)

**Overseas (China)**:
- Pros: Low cost, scalable, full-service
- Cons: Communication challenges, higher MOQs, shipping time
- Use for: High volume (>5K units)

**How to Find CMs**:
- Alibaba (search "PCB assembly")
- ThomasNet (US manufacturers)
- Referrals from other hardware startups

### Negotiation Tips

- Get quotes from 3-5 vendors
- Negotiate on MOQ, payment terms, tooling costs
- Request samples before committing
- Start small, scale with successful vendor

---

**Last Updated**: 2025-11-02
**Version**: 1.0.0
