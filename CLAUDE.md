# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Infrastructure automation for running Horizen blockchain nodes at scale. Managed 200+ secure/super nodes across OVH and Hetzner using LXD containers.

**Status:** Historical/portfolio project - the Horizen node program was discontinued in 2024.

## Architecture

### Layer 1: Terraform (`zencash-securenode/terraform/`)
Provisions LXD containers on remote hosts. Each subdirectory (sb01-sb11, sr01-sr14) represents a physical host server with container definitions.

### Layer 2: Ansible (`zencash-securenode/ansible/`)
Configuration management for nodes. Key roles:
- `zen-node` - Main role for installing zend daemon and nodetracker
- `lxd-host` - Configures physical LXD hosts
- `lockdown` - Security hardening
- `wildcard-cert` / `letsencrypt-cert` - TLS certificate management

### Layer 3: Operational Scripts (`bin/`)
Day-to-day fleet management - the tools that were actually used once infrastructure was running.

## Key Scripts

| Script | Purpose |
|--------|---------|
| `zclon` | Clone an LXD container to create a new node |
| `znew` | Configure a newly cloned node with stake address |
| `zmv` | Move/rename a node |
| `zeol` | End-of-life a node |
| `zstake` | Manage staking addresses |
| `ztc` | Tracker control (runs on nodes) |

## Configuration Files

- `zen-inv.yml` - Ansible inventory of all nodes (single source of truth)
- Terraform uses Jinja2 templates (`lxd-tf.j2`, `lxd-tf6.j2`) with Python generators to create per-host .tf files

## Network Architecture

- Dual-stack IPv4/IPv6 addressing
- LXD containers use macvlan networking for direct IPs
- Container naming: `zen-XXX` (alphanumeric based on host)
