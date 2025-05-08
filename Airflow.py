import math
from textx import metamodel_from_file

# Constants
R = 287.15  # J/(kg·K), specific gas constant for air

def init_Values(code):
    metaModel = metamodel_from_file('HighSpeed.tx')
    return metaModel.model_from_file(code)

def airflowCalculations(model):
    for input in model.inputs:
        print(f"\n--- Calculating for block: {input.name} ---")

        # Initialize as None
        pressure = None
        temperature = None
        density = None

        # Extract the properties
        for prop in input.properties:
            print(f"Read property: {prop.name} = {prop.value}")  # <- Confirm parsing

            match prop.name:
                case "InitialPressure":
                    pressure = prop.value
                case "InitialTemperature":
                    temperature = prop.value
                case "InitialDensity":
                    density = prop.value

        # Now determine which is missing and calculate it
        if pressure is None and temperature is not None and density is not None:
            pressure = density * R * temperature
            print(f"Calculated Pressure: {pressure:.2f} Pa")

        elif temperature is None and pressure is not None and density is not None:
            temperature = pressure / (density * R)
            print(f"Calculated Temperature: {temperature:.2f} K")

        elif density is None and pressure is not None and temperature is not None:
            density = pressure / (R * temperature)
            print(f"Calculated Density: {density:.5f} kg/m^3")

        else:
            print("Error: Need exactly two of Pressure, Temperature, or Density.")

def main():
    model = init_Values('normalShock.volatus')
    airflowCalculations(model)

if __name__ == "__main__":
    main()
