# Cocu Matei-Iulian - 152
from tema_3.script.tasks import CFG, string_generator, membership_derivation

if __name__ == "__main__":
    cfg = CFG()
    cfg.set_start_symbol("S")
    cfg.add_production("aSb")
    cfg.add_production("ε")

    print("="*10, end="")
    print("CFG INFORMATION", end="")
    print("="*10)
    cfg.print_cfg()
    cfg.print_cfg_info()
    print()
    print("="*10, end="")
    print("STRING GENERATOR", end="")
    print("="*9)
    string_generator(cfg)
    print()
    print("="*10, end="")
    print("DERIVATION", end="")
    print("="*15)
    membership_derivation(cfg, "aaaaaabbbbbb")
