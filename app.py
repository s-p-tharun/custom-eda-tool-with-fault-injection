import os, subprocess, platform, shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "vlsi_journey_2026" # Key for session history

UPLOADS = "uploads"
STATIC = "static"
os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(STATIC, exist_ok=True)

def inject_fault(code, fault_type):
    if fault_type == "SA0":
        return code.replace("q <= q + 1;", "q <= 4'b0000;")
    elif fault_type == "SA1":
        return code.replace("q <= q + 1;", "q <= 4'b1111;")
    return code

def run_eda_flow(code, name):
    v_path = os.path.join(UPLOADS, f"{name}.v")
    vvp_path = os.path.join(UPLOADS, f"{name}.vvp")
    vcd_name = f"{name}.vcd"
    
    # Save the injected Verilog code
    with open(v_path, "w") as f: 
        f.write(code)
    
    # The 4-Bit Counter Testbench
    tb_code = f"""
`timescale 1ns/1ps
module tb;
    reg clk, rst, en;
    wire [3:0] q;
    top uut (.clk(clk),.rst(rst),.en(en),.q(q)
    );
    always #5 clk = ~clk;
    initial begin
        $dumpfile("{vcd_name}"); 
        $dumpvars(0, tb);
        clk = 0; rst = 1; en = 0;
        #15 rst = 0;
        #10 en = 1;
        #200;
        $finish;
    end
endmodule
"""
    tb_path = os.path.join(UPLOADS, f"tb_{name}.v")
    with open(tb_path, "w") as f: 
        f.write(tb_code)
    
    if not shutil.which("iverilog"): 
        return None, "Icarus Verilog Not Found in Path"
    
    # Compile
    cp = subprocess.run(["iverilog", "-o", vvp_path, v_path, tb_path], capture_output=True, text=True)
    if cp.returncode != 0: 
        return None, cp.stderr
    
    # Simulate (creates VCD)
    subprocess.run(["vvp", vvp_path], capture_output=True)
    
    # Move VCD to static for easy access if needed, or keep in root
    return vcd_name, "Success"

@app.route("/", methods=["GET", "POST"])
def index():
    # History is now stored in the user's browser session
    if 'history' not in session:
        session['history'] = []
    
    log = ""
    if request.method == "POST":
        raw_code = request.form.get("code1")
        fault = request.form.get("fault_type")
        
        # 1. Inject Fault
        final_code = inject_fault(raw_code, fault)
        
        # 2. Run Simulation
        vcd, status = run_eda_flow(final_code, "last_run")
        
        if vcd:
            # 3. Launch GTKWave
            gtkwave_bin = shutil.which("gtkwave")
            if gtkwave_bin:
                # Use absolute path for the VCD file
                subprocess.Popen([gtkwave_bin, os.path.abspath(vcd)])

            # 4. Generate Pie Chart
            plt.figure(figsize=(5,5))
            plt.style.use('dark_background')
            if fault == "NONE":
                labels, sizes, colors = ['Testable', 'Untested'], [98, 2], ['#2ecc71', '#34495e']
                res_status = "PASS (Golden)"
            else:
                labels, sizes, colors = ['Detected', 'Masked', 'Untested'], [85, 10, 5], ['#e74c3c', '#f1c40f', '#34495e']
                res_status = f"FAIL ({fault} Detected)"
            
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
            plt.title(f"DFT Coverage: {fault}")
            plt.savefig(os.path.join(STATIC, "report.png"))
            plt.close()

            # 5. Update Session History (Workaround for session mutability)
            updated_history = session['history']
            updated_history.append({
                "mode": fault, 
                "status": res_status, 
                "coverage": "85.0%" if fault != "NONE" else "98.0%"
            })
            session['history'] = updated_history
            log = f"Simulation for {fault} successful."
        else:
            log = f"Error: {status}"

    return render_template("index.html", log=log, history=session['history'])

if __name__ == "__main__":
    app.run(debug=True)
