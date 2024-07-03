import pandas

if __name__ == "__main__":
    dataset = pandas.read_csv("data/radar.csv")
    MILD = list(dataset["MILD"])
    MOD = list(dataset["MOD"])
    SEV = list(dataset["SEV"])
    NONE = list(dataset["NONE"])
    print(f"MILD: 0 = {MILD.count(0)} 1 = {MILD.count(1)}")
    print(f"MOD: 0 = {MOD.count(0)} 1 = {MOD.count(1)}")
    print(f"SEV: 0 = {SEV.count(0)} 1 = {SEV.count(1)}")
    print(f"NONE: 0 = {NONE.count(0)} 1 = {NONE.count(1)}")