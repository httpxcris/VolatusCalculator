import math
from textx import metamodel_from_file

# Constants
R = 287.15
gamma = 1.4  # air

def init_Values(code):
    metaModel = metamodel_from_file('HighSpeed.tx')
    return metaModel.model_from_file(code)

def airflowCalculations(model):
    for input in model.inputs:
        print(f"\n--- Calculating for block: {input.name} ---")

        # Initialize values
        pressure = None
        temperature = None
        density = None
        mach = None

        # Extract input properties
        for prop in input.properties:
            print(f"Read property: {prop.name} = {prop.value}")
            match prop.name:
                case "InitialPressure":
                    pressure = prop.value
                case "InitialTemperature":
                    temperature = prop.value
                case "InitialDensity":
                    density = prop.value
                case "MachNumber":
                    mach = prop.value

        # Thermodynamic calculations
        if pressure is None and temperature is not None and density is not None:
            pressure = density * R * temperature
            print(f"Calculated Pressure: {pressure:.2f} Pa")

        elif temperature is None and pressure is not None and density is not None:
            temperature = pressure / (density * R)
            print(f"Calculated Temperature: {temperature:.2f} K")

        elif density is None and pressure is not None and temperature is not None:
            density = pressure / (R * temperature)
            print(f"Calculated Density: {density:.5f} kg/m^3")

        # Normal shock calculations
        if pressure is not None and mach is not None and mach > 1:
            P2 = pressure * (1 + (2 * gamma / (gamma + 1)) * (mach**2 - 1))
            print(f"Calculated Exit Pressure (P2) after shock: {P2:.2f} Pa")

            if temperature is not None:
                term1 = (2 * gamma * mach**2 - (gamma - 1))
                term2 = ((gamma - 1) * mach**2 + 2)
                denom = (gamma + 1)**2 * mach**2
                T2 = temperature * (term1 * term2) / denom
                print(f"Calculated Exit Temperature (T2) after shock: {T2:.2f} K")
            else:
                print("Initial temperature missing. Cannot compute T2.")

        elif mach is not None and mach <= 1:
            print("Mach number must be > 1 for normal shocks.")
        elif mach is None:
            print("Mach number not provided. Skipping shock calculations.")
        elif pressure is None:
            print("Initial pressure missing. Cannot calculate exit pressure.")

def main():
    model = init_Values('NormalShock.volatus')
    airflowCalculations(model)

if __name__ == "__main__":
    main()
