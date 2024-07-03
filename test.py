import numpy, pandas, random

if __name__ == "__main__":
    PHQ = numpy.array([random.randint(20,27) for _ in range(50)])
    GAD = numpy.array([random.randint(0,14) for _ in range(50)])
    BDI = numpy.array([random.randint(1,19) for _ in range(50)])
    PSQI = numpy.array([random.randint(0,10) for _ in range(50)])
    AFI = numpy.array([random.randint(0,7) for _ in range(50)])
    df = pandas.DataFrame({
        "PHQ": PHQ,
        "GAD": GAD,
        "BDI": BDI,
        "PSQI": PSQI,
        "AFI": AFI
    })
    df.to_csv("data/radar_out_PHQ.csv")