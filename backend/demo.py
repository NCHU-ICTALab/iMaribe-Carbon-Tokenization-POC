from . import ledger, service


def main():
    ledger.init_db()
    print("① 依核發請求批次發行 SU…")
    res = service.issue_from_requests("data/out/minting_requests.json")
    print(f"   發行 {res['count']} 筆、合計 {res['total_tonnes']} 噸")

    # 取第一個可上架（held）的 SU 當主角；乾淨鏈上就是 #0，
    # 但若 make test-backend 先燒掉 #0，這裡自動改用下一個可用的，不會卡死
    held = [s["token_id"] for s in ledger.all_su(service.client) if s["status"] == "held"]
    if not held:
        raise SystemExit("帳本裡沒有可上架的 SU，請確認鏈已重置並跑過 make data")
    tid = held[0]

    print(f"② 航商 A 把第 {tid} 號 SU 以 300 mUSD 上架…")
    service.list_su(tid, 300)

    print(f"③ 產業買方買下第 {tid} 號…")
    service.buy_su(tid)

    print(f"④ 買方除役第 {tid} 號、抵 Scope 3（purpose=3）…")
    service.retire_su(tid, 3)

    print("\n=== 本地帳本（前 10 筆）===")
    sus = ledger.all_su(service.client)
    for s in sus[:10]:
        print(f"  SU#{s['token_id']} ship={s['ship_id']} amount={s['amount']}t "
              f"owner={s['owner_role']} status={s['status']} purpose={s['purpose_name']}")
    print(f"  …共 {len(sus)} 筆、合計 {sum(s['amount'] for s in sus)} 噸")


if __name__ == "__main__":
    main()
