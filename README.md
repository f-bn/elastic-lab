<div align="center">
  <img src="assets/logo-elastic.png" alt="elastic-logo" title="elastic" height="160" />

  ---

</div>

## 📋 Overview

This repository contains an Elastic Stack lab for learning and testing purposes (with Kibana and Logstash).

## 🚀 Quick Start

### Prerequisites

Before getting started, ensure you have installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Mise](https://mise.jdx.dev/)

> [!NOTE]
> Mise is optional but **highly** recommended because some helpers commands and environment variables are managed through it for ease of management.

### Setup

First, we need to setup the environment (this):

```bash
mise setup
```

### Provisioning

Once the prerequisites are installed, we can simply launch the environment provisioning:

```bash
mise start
```

Finally, you can access the Kibana console once the cluster is bootstrapped:

```bash
mise ui
```

### Sample dataset example

In the [`datasets`](./datasets/) folder, there is a small example `recipes` dataset available for querying ElasticSearch (including mappings). This is a dataset from [Kaggle](https://www.kaggle.com/datasets/hugodarwood/epirecipes) converted in NDJSON format for insertion in ElasticSearch.

First, extract the compressed archive:

```bash
mise dataset:extract datasets/recipes.tar.gz
```

Then, load the dataset using the [loader script](./scripts/load_dataset.py):

```bash
mise dataset:load datasets/recipes.ndjson -s datasets/recipes-mappings.json -i recipes
```

### Versions management

Stack services versions are managed in the [mise.toml](./mise.toml) file in the `env` section. These variables are loaded directly in shell environment variables by Mise once entering the stack folder.

```toml
[env]
ES_VERSION = "9.5.1"
LOGSTASH_VERSION = "9.5.1"
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

**Cluster management**
* `cluster:health` - Retrieve cluster health report

**Licensing**
* `license:start-trial` - Start a 30-day trial, which gives access to all subscription features
* `license:info` - Get license information

**Datasets management**
* `dataset:extract` - Extract dataset archive
* `dataset:load` - Load dataset data into an ElasticSearch index

**Misc**
* `ui` - Open Kibana console in browser
