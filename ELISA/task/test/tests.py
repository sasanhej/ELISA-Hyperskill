import pandas as pd
from hstest import *
import os

standard_values = """Samples,OD1,OD2,Concentration (ng/ml)\nSTD1,0.319,0.315,2.058\nSTD2,0.618,0.463,6.173\nSTD3,0.675,0.69,18.519\nSTD4,0.847,0.851,55.556\nSTD5,1.025,1.008,166.667\nSTD6,0.97,0.975,500.0"""

elisa_testing = """Sample,OD1,OD2\nSample1,0.493,0.391\nSample2,0.330,0.345\nSample3,0.337,0.387\nSample4,0.372,0.366\nSample5,0.208,0.394\nSample6,0.396,0.372\nSample7,0.378,0.359\nSample8,0.317,0.356\nSample9,0.456,0.502\nSample10,0.509,0.387\nBLANK,0.110,0.135"""

elisa_data = """Sample,OD1,OD2\nSample1,0.443,0.488\nSample2,0.433,0.43\nSample3,0.343,0.351\nSample4,0.39,0.354\nSample5,0.451,0.435\nSample6,0.408,0.371\nSample7,0.372,0.36\nSample8,0.326,0.333\nSample9,0.453,0.423\nSample10,0.352,0.379\nBLANK,0.11,0.135"""


class TestUserProgram(StageTest):
    @dynamic_test(files={"test/elisa_data.csv": elisa_data, "test/standard_values.csv": standard_values})
    def test(self):
        main = TestedProgram()
        main.start()
        if not main.is_waiting_input():
            return CheckResult.wrong("You should not input any data")
        main.execute("test/elisa_data.csv")
        main.execute("test/standard_values.csv")
        path = "elisa_result.csv"
        result = [True, True, False, True, True, True, True, False, True, True, False]
        if not os.path.exists(path):
            return CheckResult.wrong("File 'elisa_result.csv' could not be found!")
        df = pd.read_csv("elisa_result.csv")
        if "AverageOD" and "CorrectedOD" not in df.columns:
            return CheckResult.wrong("Your DataFrame should have 'AverageOD' and 'CorrectedOD' columns!")
        elif "Concentration (ng/ml)" not in df.columns:
            return CheckResult.wrong("Your DataFrame should have a 'Concentration (ng/ml)' column!")
        elif "Protein detectable" not in df.columns:
            return CheckResult.wrong("Your DataFrame should have a 'Protein detectable' column!")
        elif result != df['Protein detectable'].to_list():
            return CheckResult.wrong("'Protein detectable' column has wrong values.")
        else:
            return CheckResult.correct()


if __name__ == '__main__':
    TestUserProgram().run_tests()



