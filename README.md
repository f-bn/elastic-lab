<div align="center">
  <img src="assets/logo-elastic.png" alt="elastic-logo" title="elastic" height="200" />

  ---

</div>

## 📋 Overview

This repository contains an ElasticSearch stack (with Kibana) for learning and testing purposes.

## 🚀 Quick Start

### Prerequisites

Before getting started, ensure you have [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/) and [Mise](https://mise.jdx.dev/) installed.

> [!NOTE]
> Mise is optional but some helpers commands and environment variables are managed via Mise for ease of management.

### Provisionning

Once the prerequisites are installed, we can simply launch the environment provisionning:

* With Mise:

  ```bash
  mise start
  ```

* Or with `docker compose`:

  ```bash
  docker compose up -d
  ```

Finally, you can access the Kibana console:

```bash
mise kibana
```

### Versions management

Stack services versions are managed in the [mise.toml](./mise.toml) file in the `env` section. These variables are loaded directly in shell environment variables by Mise once entering the stack folder.

```toml
[env]
# ElasticSearch
ES_VERSION = "9.5.1"

# Kibana
KIBANA_VERSION = "9.5.1"
```

### Mise tasks available

All common operations are wrapped in **Mise** tasks to provide a consistent and convenient interface instead of memorizing long `docker-compose` or `curl` commands.

**Stack management**
* `start` - Start stack
* `stop` - Stop stack
* `clean` - Clean all stack resources (services, volumes, networks)
* `reset` - Reset stack from scratch

**Service management**
* `logs` - Get logs from a given stack service

**License**
* `start-trial` - Start a 30-day trial, which gives access to all subscription features

**Misc**
* `kibana` - Open Kibana console in browser