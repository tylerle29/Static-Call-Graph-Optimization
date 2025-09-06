import json
import sys

def load_call_graph(path):
    with open(path) as f:
        return json.load(f)

def method_signature(method):
    return f"{method['declaringClass']}::{method['name']}({','.join(method['parameterTypes'])}) -> {method['returnType']}"

def callsite_id(site):
    return f"line={site.get('line','?')},pc={site.get('pc','?')}"

def target_signature(target):
    return f"{target['declaringClass']}::{target['name']}({','.join(target['parameterTypes'])}) -> {target['returnType']}"

def compare_call_graphs(g1, g2, g3, g4, g5, g6, g7):
    methods1 = {method_signature(m['method']): m for m in g1['reachableMethods']}
    methods2 = {method_signature(m['method']): m for m in g2['reachableMethods']}
    methods3 = {method_signature(m['method']): m for m in g3['reachableMethods']}
    methods4 = {method_signature(m['method']): m for m in g4['reachableMethods']}
    methods5 = {method_signature(m['method']): m for m in g5['reachableMethods']}
    methods6 = {method_signature(m['method']): m for m in g6['reachableMethods']}
    methods7 = {method_signature(m['method']): m for m in g7['reachableMethods']}


    all_methods = sorted(set(methods1) | set(methods2) | set(methods3) | set(methods4) | set(methods5) | set(methods6) | set(methods7))
    shared_methods = set(methods1) & set(methods2) & set(methods3) & set(methods4) & set(methods5) & set(methods6) & set(methods7)


    diff = {
        "methods_only_in_graph1": sorted(set(methods1) - shared_methods),
        "methods_only_in_graph2": sorted(set(methods2) - shared_methods),
        "methods_only_in_graph3": sorted(set(methods3) - shared_methods),
        "methods_only_in_graph4": sorted(set(methods4) - shared_methods),
        "methods_only_in_graph5": sorted(set(methods5) - shared_methods),
        "methods_only_in_graph6": sorted(set(methods6) - shared_methods),
        "methods_only_in_graph7": sorted(set(methods7) - shared_methods),
        "callsite_differences": {},
        "summary": {}
    }

    for method_sig in shared_methods:
        m1 = methods1[method_sig]
        m2 = methods2[method_sig]
        m3 = methods3[method_sig]
        m4 = methods4[method_sig]
        m5 = methods5[method_sig]
        m6 = methods6[method_sig]
        m7 = methods7[method_sig]

        sites1 = {callsite_id(cs): cs for cs in m1.get("callSites", [])}
        sites2 = {callsite_id(cs): cs for cs in m2.get("callSites", [])}
        sites3 = {callsite_id(cs): cs for cs in m3.get("callSites", [])}
        sites4 = {callsite_id(cs): cs for cs in m4.get("callSites", [])}
        sites5 = {callsite_id(cs): cs for cs in m5.get("callSites", [])}
        sites6 = {callsite_id(cs): cs for cs in m6.get("callSites", [])}
        sites7 = {callsite_id(cs): cs for cs in m7.get("callSites", [])}
        all_sites = set(sites1) | set(sites2) | set(sites3) | set(sites4) | set(sites5) | set(sites6) | set(sites7)

        site_diffs = {}

        for sid in all_sites:
            cs1 = sites1.get(sid)
            cs2 = sites2.get(sid)
            cs3 = sites3.get(sid)
            cs4 = sites4.get(sid)
            cs5 = sites5.get(sid)
            cs6 = sites6.get(sid)
            cs7 = sites7.get(sid)

            targets1 = {target_signature(t) for t in cs1.get("targets", [])} if cs1 else set()
            targets2 = {target_signature(t) for t in cs2.get("targets", [])} if cs2 else set()
            targets3 = {target_signature(t) for t in cs3.get("targets", [])} if cs3 else set()
            targets4 = {target_signature(t) for t in cs4.get("targets", [])} if cs4 else set()
            targets5 = {target_signature(t) for t in cs5.get("targets", [])} if cs5 else set()
            targets6 = {target_signature(t) for t in cs6.get("targets", [])} if cs6 else set()
            targets7 = {target_signature(t) for t in cs7.get("targets", [])} if cs7 else set()


            site_diffs[sid] = {
                "targets_only_in_graph1": sorted(targets1 - targets2 - targets3 - targets4 - targets5 - targets6 - targets7),
                "targets_only_in_graph2": sorted(targets2 - targets1 - targets3 - targets4 - targets5 - targets6 - targets7),
                "targets_only_in_graph3": sorted(targets3 - targets1 - targets2 - targets4 - targets5 - targets6 - targets7),
                "targets_only_in_graph4": sorted(targets4 - targets1 - targets2 - targets3 - targets5 - targets6 - targets7),
                "targets_only_in_graph5": sorted(targets5 - targets1 - targets2 - targets3 - targets4 - targets6 - targets7),
                "targets_only_in_graph6": sorted(targets6 - targets1 - targets2 - targets3 - targets4 - targets5 - targets7),
                "targets_only_in_graph7": sorted(targets7 - targets1 - targets2 - targets3 - targets4 - targets5 - targets6),
                "shared_targets": sorted(targets1 & targets2 & targets3 & targets4 & targets5 & targets6 & targets7)
            }
        # --- Target similarity calculation ---
    total_targets_graph1 = set()
    total_targets_graph2 = set()
    total_targets_graph3 = set()
    total_targets_graph4 = set()
    total_targets_graph5 = set()
    total_targets_graph6 = set()
    total_targets_graph7 = set()
    shared_targets_total = set()

    for method_sig in shared_methods:
        m1 = methods1[method_sig]
        m2 = methods2[method_sig]
        m3 = methods3[method_sig]
        m4 = methods4[method_sig]
        m5 = methods5[method_sig]
        m6 = methods6[method_sig]
        m7 = methods7[method_sig]

        sites1 = {callsite_id(cs): cs for cs in m1.get("callSites", [])}
        sites2 = {callsite_id(cs): cs for cs in m2.get("callSites", [])}
        sites3 = {callsite_id(cs): cs for cs in m3.get("callSites", [])}
        sites4 = {callsite_id(cs): cs for cs in m4.get("callSites", [])}
        sites5 = {callsite_id(cs): cs for cs in m5.get("callSites", [])}
        sites6 = {callsite_id(cs): cs for cs in m6.get("callSites", [])}
        sites7 = {callsite_id(cs): cs for cs in m7.get("callSites", [])}

        all_sites = set(sites1) | set(sites2) | set(sites3) | set(sites4) | set(sites5) | set(sites6) | set(sites7)

        for sid in all_sites:
            cs1 = sites1.get(sid)
            cs2 = sites2.get(sid)
            cs3 = sites3.get(sid)
            cs4 = sites4.get(sid)
            cs5 = sites5.get(sid)
            cs6 = sites6.get(sid)
            cs7 = sites7.get(sid)

            targets1 = {target_signature(t) for t in cs1.get("targets", [])} if cs1 else set()
            targets2 = {target_signature(t) for t in cs2.get("targets", [])} if cs2 else set()
            targets3 = {target_signature(t) for t in cs3.get("targets", [])} if cs3 else set()
            targets4 = {target_signature(t) for t in cs4.get("targets", [])} if cs4 else set()
            targets5 = {target_signature(t) for t in cs5.get("targets", [])} if cs5 else set()
            targets6 = {target_signature(t) for t in cs6.get("targets", [])} if cs6 else set()
            targets7 = {target_signature(t) for t in cs7.get("targets", [])} if cs7 else set()

            total_targets_graph1.update(targets1)
            total_targets_graph2.update(targets2)
            total_targets_graph3.update(targets3)
            total_targets_graph4.update(targets4)
            total_targets_graph5.update(targets5)
            total_targets_graph6.update(targets6)
            total_targets_graph7.update(targets7)
            shared_targets_total.update(targets1 & targets2 & targets3 & targets4 & targets5 & targets6 & targets7)

    all_unique_targets = total_targets_graph1 | total_targets_graph2 | total_targets_graph3 | total_targets_graph4 | total_targets_graph5 | total_targets_graph6 | total_targets_graph7
    target_similarity_ratio = len(shared_targets_total) / len(all_unique_targets) if all_unique_targets else 1.0

    
    if site_diffs:
        diff["callsite_differences"][method_sig] = site_diffs

    # Add summary
    diff["summary"] = {
        "total_methods_graph1": len(methods1),
        "total_methods_graph2": len(methods2),
        "shared_methods": len(shared_methods),
        "total_unique_methods": len(all_methods),
        "method_similarity_ratio": round(len(shared_methods) / len(all_methods), 4),
        "methods_only_in_graph1": len(diff["methods_only_in_graph1"]),
        "methods_only_in_graph2": len(diff["methods_only_in_graph2"]),
        "methods_only_in_graph3": len(diff["methods_only_in_graph3"]),
        "methods_only_in_graph4": len(diff["methods_only_in_graph4"]),
        "methods_only_in_graph5": len(diff["methods_only_in_graph5"]),
        "methods_only_in_graph6": len(diff["methods_only_in_graph6"]),
        "methods_only_in_graph7": len(diff["methods_only_in_graph7"]),
        "methods_with_target_differences": len(diff["callsite_differences"])
    }

    diff["summary"]["target_similarity_ratio"] = round(target_similarity_ratio, 4)
    diff["summary"]["total_unique_targets"] = len(all_unique_targets)
    diff["summary"]["shared_targets"] = len(shared_targets_total)


    return diff

def print_diff(diff):
    print("=== Method Differences ===")
    print("\nMethods only in Graph 1:")
    for m in diff["methods_only_in_graph1"]:
        print("  -", m)

    print("\nMethods only in Graph 2:")
    for m in diff["methods_only_in_graph2"]:
        print("  -", m)

    print("\n=== Target Differences in Shared Methods ===")
    for method, sites in diff["callsite_differences"].items():
        print(f"\nMethod: {method}")
        for site_id, site_diff in sites.items():
            print(f"  Call Site: {site_id}")
            if site_diff["targets_only_in_graph1"]:
                print("    Targets only in Graph 1:")
                for t in site_diff["targets_only_in_graph1"]:
                    print("      →", t)
            if site_diff["targets_only_in_graph2"]:
                print("    Targets only in Graph 2:")
                for t in site_diff["targets_only_in_graph2"]:
                    print("      →", t)

    print("\n=== Summary ===")
    for key, value in diff["summary"].items():
        print(f"  {key}: {value}")

def main():
    g1 = load_call_graph("cg.json")
    g2 = load_call_graph("cg_og.json")
    g3 = load_call_graph("cg_og_xalan.json")
    g4 = load_call_graph("cg_og_xalan_1.json")
    g5 = load_call_graph("cg_og_xalan_2.json")
    g6 = load_call_graph("cg_xalan_3.json")
    g7 = load_call_graph("cg_og_xalan_4.json")


    differences = compare_call_graphs(g1, g2, g3, g4, g5, g6, g7)
    with open("callgraph_diff.json", "w", encoding="utf-8") as f_json:
        json.dump(differences, f_json, indent=2)

    print_diff(differences)

if __name__ == "__main__":
    main()
