🛠️ CUSTOM-EDA-TOOL-WITH-FAULT-INJECTION
📌 Project Overview
This project is a custom Electronic Design Automation (EDA) tool designed to automate Fault Injection in RTL designs. Built as an entry point into the Design For Testability (DFT) domain, the tool allows users to simulate physical manufacturing defects (Stuck-At Models) and visualize their impact on digital logic.

The tool currently supports a 4-bit Synchronous Counter as the primary Unit Under Test (UUT), demonstrating how internal faults can mask functionality despite healthy control signals.

🏗️ Technical Stack
Frontend: Flask & HTML (Web-based GUI for simulation control)

Backend Engine: Python (Automated Verilog source manipulation for fault injection)

Simulator: Icarus Verilog (HDL Compilation and Execution)

Waveform Viewer: GTKWave (VCD file visualization)

🧪 Supported Fault Models
Golden Run: Simulates the design in its ideal, functional state.

Stuck-At-0 (SA0): Mimics a signal line shorted to Ground (VSS).

Stuck-At-1 (SA1): Mimics a signal line shorted to Power (VDD).

🚀 Getting Started
Prerequisites
Ensure you have the following installed:

Python 3.x

Icarus Verilog (iverilog)

GTKWave

Installation
Clone the repository:

Bash
cd RTL-Fault-Injector
Install dependencies:
Bash
pip install flask
Run the application:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000.

📈 Observations
By injecting a Stuck-At-0 fault into a 4-bit counter, the tool demonstrates a lack of Observability. While the clk and en signals toggle correctly in the testbench, the output q remains locked at zero, simulating a silent hardware failure.

🗺️ Roadmap
[ ] Gate-Level Injection: Integrating Yosys for post-synthesis fault injection.

[ ] Automated Coverage: Scripting a loop to calculate the exact % of faults detected by the testbench.

[ ] Scan Chain Integration: Modifying RTL to include Scan Flip-Flops for improved controllability.
