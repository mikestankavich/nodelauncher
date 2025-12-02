# NodeLauncher

**Horizen (ZEN) node hosting business, 2018-2024** | [nodelauncher.com](https://nodelauncher.com)

NodeLauncher operated ~200 Horizen secure/super nodes across multiple geographic regions until the [protocol deprecated the node model](https://blog.horizen.io/secure-node-full-deprecation-timeline-eon-forger-node-instructions/) in favor of EON forger nodes in 2024.

This repository contains the infrastructure automation and operational tooling that managed the fleet.

## The Story

**Origin**: A crypto investment club did a group buy into Horizen. Node setup required Linux CLI skills most members didn't have. I saw the gap, offered to host nodes for club members, and quickly realized the business opportunity.

**Growth**: Word of mouth, Horizen Discord presence, and a listing on Horizen's official node hosting providers guide. WordPress/WooCommerce storefront, PayPal payments (Stripe banned crypto). Scaled to ~200 nodes across 10-12 bare metal servers, ~$2K/month peak revenue.

**End**: Horizen deprecated secure/super nodes in favor of EON forger nodes (stake-weighted validators). The business model evaporated—not an execution failure, just platform risk. Professional shutdown with customer notice.

**Six years, profitable throughout, real customers with low churn** (most left due to exiting ZEN, not service issues).

## Infrastructure Decisions

These weren't textbook choices—they were driven by unit economics at $10-12/node:

| Decision | Rationale |
|----------|-----------|
| **LXD containers, not VMs** | Needed density. VMs couldn't hit the margins. |
| **Copy-on-write with dedup** | 70GB+ blockchain shared across nodes. Each node only stores deltas (wallet, config, tracker state). |
| **IPv6-only for secure nodes** | Providers charged premium for scarce IPv4 addresses. |
| **Hetzner AX61** | 128GB RAM, 2x2TB NVMe, ~$120/month. Could run 70+ nodes on single box. |
| **Right-sized for actual SLAs** | 92% secure, 96-98% super. No point engineering for 5 9s. |

### Unit Economics Evolution

| Phase | Nodes | Revenue | Unit Cost | Notes |
|-------|-------|---------|-----------|-------|
| Early | ~50 | ~$500/mo | $10-12/node | 50%+ margins |
| Peak | ~200 | ~$2K/mo | $4-5/node | IPv4 on OVH servers |
| Final | 50-60 | ~$200/mo | ~$1.60/node | IPv6-only on Hetzner AX61. Competition drove prices to $2-3/node. |

## Tooling Evolution

The infrastructure evolved through three phases:

### Phase 1: Full IaC Stack
Started with the textbook approach:
- **Terraform** for LXD container orchestration
- **Ansible** for configuration management
- **Python scripts** to bridge inventory → Terraform templates

### Phase 2: Reality Sets In
Terraform excels at managing cloud resources with stable APIs, but for LXD containers where you're doing frequent clones, migrations, and re-provisioning, the state management overhead became friction.

### Phase 3: Battle-Tested Shell Scripts
The final operational model used direct `lxc` commands wrapped in purpose-built scripts. These matched how I actually thought about the work: "clone this node", "drain that wallet", "re-stake these addresses".

## Repository Structure

```
nodelauncher/
├── bin/                    # Operational scripts (the daily drivers)
│   ├── ztc                 # Tracker control - pushed to every node
│   ├── zbals               # Balance checker - fleet-wide via Ansible
│   ├── zstake              # Batch challenge balance refills
│   ├── zclon               # Clone container from base image
│   ├── znew                # Post-clone setup with stake address
│   ├── reclon              # Rebuild node (disk recovery, fresh start)
│   ├── zmv                 # Migrate node between hosts
│   ├── destake             # Remove stake before decommission
│   ├── zeol                # End-of-life (graceful decommission)
│   └── ...
├── zencash-securenode/     # IaC components (historical)
│   ├── ansible/            # Configuration management roles
│   ├── terraform/          # LXD container definitions per host
│   ├── ovh_api/            # Dynamic inventory from OVH API
│   └── utility_scripts/    # Support tooling
└── zen-inv.yml             # Ansible inventory (single source of truth)
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `ztc` | Tracker control script pushed to every node |
| `zbals` | Check challenge balances fleet-wide |
| `zstake` | Batch stake address operations |
| `zclon` | Clone container from base image, assign IP, configure networking |
| `znew` | Post-clone setup: generate stake address, register with tracker |
| `reclon` | Re-clone a misbehaving node from fresh base |
| `zmv` | Migrate node between hosts (snapshot → transfer → restore) |
| `destake` | Remove stake from nodes being decommissioned |
| `zeol` | Graceful decommission: drain wallet, unregister, archive |

## Lessons Learned

1. **Start with the textbook approach, adapt to reality**: The Terraform → shell scripts evolution wasn't a failure—it was learning where the friction actually was.

2. **Inventory as single source of truth**: `zen-inv.yml` drove everything—Ansible, Terraform template generation, DNS updates.

3. **Lifecycle scripts matter more than provisioning**: 90% of operational time was spent on migrations, re-stakes, and troubleshooting—not initial setup.

4. **Platform risk is real**: Built a business on someone else's incentive design. When they changed the rules, the business model evaporated.

5. **Right-size for actual requirements**: The SLAs were relaxed. No point over-engineering for uptime guarantees nobody was paying for.

## Note on Credentials

All sensitive values (passwords, API keys, SSH keys) have been redacted. The structure and logic remain intact to demonstrate the operational patterns.

## Status

**Archive/Portfolio Repository** - This is a historical archive of a real business that ran from 2018-2024. The Horizen secure/super node program has ended. No nodes are currently running.

This repository is read-only. Issues and pull requests are not being accepted.

The infrastructure patterns—fleet management, container orchestration, lifecycle automation—transfer to other distributed infrastructure challenges.

## License

MIT
