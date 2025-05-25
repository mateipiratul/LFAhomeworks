from tema_3.script.tasks import CFG, string_generator, membership_derivation

def bonus_cfg(n):
    abcstar = []
    for i in range(n + 1):
        abcw = "a" * i + "b" * i + "c" * i
        abcstar.append(abcw)
    return abcstar

if __name__ == "__main__":
    cfgabc = CFG()  # trying to replicate bonus 'CFG'
    cfgabc.set_start_symbol("S")
    cfgabc.add_production("S", "aA")
    cfgabc.add_production("S", "bB")
    cfgabc.add_production("S", "cC")
    cfgabc.add_production("A", "aA")
    cfgabc.add_production("A", "ε")
    cfgabc.add_production("B", "bB")
    cfgabc.add_production("B", "ε")
    cfgabc.add_production("C", "cC")
    cfgabc.add_production("C", "ε")

    pseudocfg_gen = bonus_cfg(2**64)