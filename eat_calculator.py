# Quick script for page table math, address translation, and EAT numbers

def analyze_page_table_and_address():
    print("=========================================================")
    print(" PART 2.1: PAGE TABLE & ADDRESS TRANSLATION WALKTHROUGH")
    print("=========================================================")

    # Basic setup: 32-bit addresses, 4 KB pages, 4 bytes per entry
    va_bits = 32
    page_size_bytes = 4 * 1024  # 4096 bytes (2^12)
    pte_size_bytes = 4

    # Work out the page count and total page table size
    offset_bits = 12  # 2^12 = 4096
    vpn_bits = va_bits - offset_bits  # 32 - 12 = 20 bits
    num_pages = 2 ** vpn_bits
    page_table_bytes = num_pages * pte_size_bytes
    page_table_mb = page_table_bytes / (1024 * 1024)

    print(f"Number of Virtual Pages : {num_pages:,} (2^{vpn_bits})")
    print(f"Number of PTEs          : {num_pages:,}")
    print(f"Single-Level Table Size : {page_table_bytes:,} bytes ({page_table_mb:.2f} MB)")

    # Break down the hex address 0x00003A7C into VPN and Offset
    v_addr = 0x00003A7C
    vpn = v_addr >> offset_bits                # Grab top 20 bits
    offset = v_addr & ((1 << offset_bits) - 1)  # Grab bottom 12 bits

    print(f"\nVirtual Address (Hex)   : 0x{v_addr:08X} (Decimal: {v_addr})")
    print(f"Full 32-bit Binary      : {v_addr:032b}")
    print(f"VPN (Upper 20 bits)     : {vpn:020b} (Hex: 0x{vpn:05X}, Dec: {vpn})")
    print(f"Offset (Lower 12 bits)  : {offset:012b} (Hex: 0x{offset:03X}, Dec: {offset})")

def calculate_eat():
    print("\n=========================================================")
    print(" PART 2.2: EFFECTIVE ACCESS TIME (EAT) PERFORMANCE")
    print("=========================================================")

    # RAM access is 100 ns, page fault takes 8 ms (8,000,000 ns)
    mem_access_ns = 100.0
    fault_service_ns = 8_000_000.0

    # Fault rates to test (in percent)
    fault_rates_pct = [0.0, 0.001, 0.01, 0.1, 1.0]

    print(f"{'Fault Rate (%)':<16} | {'Prob (p)':<10} | {'EAT (ns)':<14} | {'Slowdown':<10}")
    print("-" * 58)

    for pct in fault_rates_pct:
        # Turn percentage into decimal probability p
        p = pct / 100.0
        # Plug into the EAT formula
        eat_ns = (1.0 - p) * mem_access_ns + (p * fault_service_ns)
        slowdown = eat_ns / mem_access_ns
        print(f"{pct:<15.3f}% | {p:<10.5f} | {eat_ns:<14.3f} | {slowdown:<9.2f}x")

    # Find the exact fault rate where memory gets 2x slower (200 ns)
    target_eat = 2.0 * mem_access_ns
    p_two_x = (target_eat - mem_access_ns) / (fault_service_ns - mem_access_ns)
    print("-" * 58)
    print(f"2x Slowdown Threshold (EAT = 200 ns): p = {p_two_x:.8f} ({p_two_x * 100:.5f}%)")

if __name__ == "__main__":
    analyze_page_table_and_address()
    calculate_eat()