Title: Incorporating Terraform Commands into Makefiles
Date: 2020-02-15 12:00
Category: Terraform
Tags: terraform, makefile, make, python

# Table of Contents

* [Summary](#summary)
* [Step 0: Directory and File Layout](#step-0-directory-and-file-layout)
    * [Environment Variables](#environment-variables)
* [Step 1: Top Level Makefile](#step-1-top-level-makefile)
* [Step 2: Infra Level Makefile](#step-2-infra-level-makefile)
    * [Fake Targets](#fake-targets)
    * [Commands for Single Components](#commands-for-single-components)
    * [Commands for All Components](#commands-for-all-components)
    * [Variables](#variables)
    * [Final Makefile](#final-makefile)
* [Step 3: Writing Terraform Components](#step-3-writing-terraform-components)
* [Step 4: Initializing Terraform Components](#step-4-initializing-terraform-components)
* [Workflow](#workflow)
    * [Plan](#plan)
    * [Deploy](#deploy)
    * [Update](#update)
    * [Destroy](#destroy)

# Summary

This blog post covers a useful pattern for incorporating terraform commands
into a Makefile.

This is useful for cases where terraform is being used to manage infrastructure.
In the end you will be able to run a command like

```text
make plan-infra
make deploy-infra
```

and and have this call the corresponding terraform commands to plan and deploy your
terraformed cloud infrastructure.

The post is divided into a few steps:

- Directory and file layout - how we lay out the files for this tutorial
- Top level Makefile - make commands to add to the top level Makefile
- Infra level Makefile - make commands to add to the infra level Makefile
- Writing Terraform component - how to write a configurable component that is ready to terraform
- Initializing Terraform component - script to initialize terraform components
- Workflow - plan, deploy, update, destroy

# Step 0: Directory and File Layout

This tutorial presumes you have a top level directory corresponding to a git repository.
We will use the following directory structure for this example:

```text
my-project/
    Readme.md
    environment
    Makefile
    infra/
        Makefile
        component-1/
            variables.tf
            main.tf
```

## Environment Variables

In order to keep track of environment variables used in the terraform
process, we use the file `envronment` in the top level project directory
to keep all environment variable values under version control.

```bash
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
export PROJECT_HOME="$(cd -P "$(dirname "$SOURCE")" && pwd)"

set -a
PROJECT_DEPLOYMENT_STAGE="dev"

# bucket name
PROJECT_S3_BUCKET="my-organization-my-project-my-bucket"

# aws tags
PROJECT_INFRA_TAG_PROJECT="my-project"
PROJECT_INFRA_TAG_SERVICE="my-service"
PROJECT_INFRA_TAG_OWNER="whoami@email.com"

# aws settings
AWS_DEFAULT_OUTPUT=json
AWS_DEFAULT_REGION=us-east-1
set +a
```

Optionally, a local environment file can contain environment variable values
that are sensitive or should not be kept under version control, so add this
to the bottom of the `environment` file too:

```bash
if [[ -f "${PROJECT_HOME}/environment.local" ]]; then
    source "${PROJECT_HOME}/environment.local"
fi
```

# Step 1: Top Level Makefile

Start by creating the `plan-infra` and `deploy-infra` commands in your top-level
Makefile. These commands will, in turn, call make commands defined in `infra/Makefile`:

```make
plan-infra:
	$(MAKE) -C infra plan-all

deploy-infra:
	$(MAKE) -C infra apply-all
```

The `-C infra` flag indicates make should use a Makefile in a subdirectory.

# Step 2: Infra Level Makefile

Next we define `infra/Makefile`. This Makefile will have two parts:

- terraform commands for a single component (example: init, plan, apply, destroy)
- wrapper commands to run the above commands for every component (example: for each component,
  run the plan terraform command)

We cover the Makefile from the bottom up.

## Fake Targets

Start by defining "fake" targets or rules, that is, make rules whose names are not file names:

```make
.PHONY: init-all plan-all apply-all clean-all plan apply destroy init clean
```

## Commands for Single Components

Next, above that, we define terraform commands for a single component:

```make
init:
	rm -rf $(COMPONENT)/.terraform/*.tfstate
	./build_deploy_config.py $(COMPONENT)
	cd $(COMPONENT); terraform init;

plan: init
	cd $(COMPONENT); terraform plan -detailed-exitcode

apply: init
	cd $(COMPONENT); terraform apply

destroy: init
	cd $(COMPONENT); terraform destroy

clean:
	cd $(COMPONENT); rm -rf .terraform
```

Note that the `init` command is running a `build_deploy_config.py` script,
which we will cover in a moment. This script creates the terraform variables
file `variables.tf` and populates the variable values using environment
variables.

## Commands for All Components

Above that, we have commands to perform each action on all components:

```make
all: init-all

init-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	init COMPONENT=$$c || exit 1; \
	done

plan-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	plan COMPONENT=$$c || exit 1; \
	done

apply-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	apply COMPONENT=$$c || exit 1; \
	done

destroy-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	destroy COMPONENT=$$c || exit 1; \
	done

clean-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	clean COMPONENT=$$c || exit 1; \
	done
```

## Variables

Last but not least, we define a few variables at the top of the Makefile:
most importantly, the list of infrastructure components. This is created by
extracting the names of subdirectories in `infra/` containing `*.tf` files:

```make
DIRS=${shell find . -name "*.tf" -exec dirname {} \; | sort --unique}
COMPONENTS=${shell for d in $(DIRS); do basename $$d; done}
```

## Final Makefile

Here is the final `infra/Makefile`:

**`infra/Makefile`:**

```make
DIRS=${shell find . -name "*.tf" -exec dirname {} \; | sort --unique}
COMPONENTS=${shell for d in $(DIRS); do basename $$d; done}

all: init-all

init-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	init COMPONENT=$$c || exit 1; \
	done

plan-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	plan COMPONENT=$$c || exit 1; \
	done

apply-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	apply COMPONENT=$$c || exit 1; \
	done

destroy-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	destroy COMPONENT=$$c || exit 1; \
	done

clean-all:
	@for c in $(COMPONENTS); do \
		$(MAKE)	clean COMPONENT=$$c || exit 1; \
	done

plan: init
	cd $(COMPONENT); terraform plan -detailed-exitcode

apply: init
	cd $(COMPONENT); terraform apply

destroy: init
	cd $(COMPONENT); terraform destroy

init:
	rm -rf $(COMPONENT)/.terraform/*.tfstate
	./build_deploy_config.py $(COMPONENT)
	cd $(COMPONENT); terraform init;

clean:
	cd $(COMPONENT); rm -rf .terraform

.PHONY: init-all plan-all apply-all clean-all plan apply destroy init clean
```

# Step 3: Writing Terraform Components

As an example, we will consider an example of terraform-managed buckets.

Start by creating a directory called `infra/buckets/` to store terraform
files for creating and managing the buckets.

We can create one file per cloud provider. As an example, here is `s3.tf`:

**`s3.tf`**:

```text
data "aws_caller_identity" "current" {}

locals {
  common_tags = "${map(
    "project"   , "${var.PROJECT_INFRA_TAG_PROJECT}",
    "env"       , "${var.PROJECT_DEPLOYMENT_STAGE}",
    "service"   , "${var.PROJECT_INFRA_TAG_SERVICE}"
  )}"
  aws_tags = "${map(
  "Name"      , "${var.PROJECT_INFRA_TAG_SERVICE}-s3-storage",
  "owner"     , "${var.PROJECT_INFRA_TAG_OWNER}",
  "managedBy" , "terraform"
  )}"
}

resource aws_s3_bucket dss_s3_bucket {
  count = length(var.PROJECT_S3_BUCKET) > 0 ? 1 : 0
  bucket = var.PROJECT_S3_BUCKET
  server_side_encryption_configuration {
    rule {
	  apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  tags = merge(local.common_tags, local.aws_tags)
}

```

Note that this requires several environment variables to be
defined in `environment` and requires the operator to run:

```text
source environment
```

# Step 4: Initializing Terraform Components

The following script will automatically generate terraform files for
our component that are populated with the correct environment variable
values.

It is called `build_deploy_config.py`.

Start with a simple argument parser that just accepts a single argument,
the component to make terraform files for:

```python
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("component")
args = parser.parse_args()
```

Next, we define several terraform file templates using Python's
bracket template syntax. Start with a template for defining a
terraform variable:

```text
terraform_variable_template = """
variable "{name}" {{
  default = "{val}"
}}
"""
```

Next, define a template for the terraform backend buket:

```text
terraform_backend_template = """# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.
terraform {{
  backend "s3" {{
    bucket = "{bucket}"
    key = "{comp}-{stage}.tfstate"
    region = "{region}"
    {profile_setting}
  }}
}}
"""
```

Next define terraform cloud providers:

```text
terraform_providers_template = """# Auto-generated during infra build process.
# Please edit infra/build_deploy_config.py directly.
provider aws {{
  region = "{aws_region}"
}}
"""
```

Provide a list of environment variables that should also be defined as
terraform variables:

```bash
env_vars_to_infra = [
PROJECT_DEPLOYMENT_STAGE="dev"

# bucket name
PROJECT_S3_BUCKET="my-organization-my-project-my-bucket"

# aws tags
PROJECT_INFRA_TAG_PROJECT="my-project"
PROJECT_INFRA_TAG_SERVICE="my-service"
PROJECT_INFRA_TAG_OWNER="whoami@email.com"

# aws settings
AWS_DEFAULT_OUTPUT=json
AWS_DEFAULT_REGION=us-east-1

    "AWS_DEFAULT_REGION",
    "PROJECT_DEPLOYMENT_STAGE",
    "PROJECT_S3_BUCKET",
    "PROJECT_INFRA_TAG_PROJECT",
    "PROJECT_INFRA_TAG_SERVICE",
    "PROJECT_INFRA_TAG_OWNER"
]
```

Finally, substitute environment variable values into the templates, and write
the templated content to the appropriate `*.tf` file. First, the backend:

```python
# Write backend.tf
with open(os.path.join(infra_root, args.component, "backend.tf"), "w") as fp:
    caller_info = boto3.client("sts").get_caller_identity()
    if os.environ.get('AWS_PROFILE'):
        profile = os.environ['AWS_PROFILE']
        profile_setting = f'profile = "{profile}"'
    else:
        profile_setting = ''
    fp.write(terraform_backend_template.format(
        bucket=os.environ['DSS_TERRAFORM_BACKEND_BUCKET_TEMPLATE'].format(account_id=caller_info['Account']),
        comp=args.component,
        stage=os.environ['DSS_DEPLOYMENT_STAGE'],
        region=os.environ['AWS_DEFAULT_REGION'],
        profile_setting=profile_setting,
    ))
```

Next, the `variables.tf` for the component:

```python
# Write variables.tf
with open(os.path.join(infra_root, args.component, "variables.tf"), "w") as fp:
    fp.write("# Auto-generated during infra build process." + os.linesep)
    fp.write("# Please edit infra/build_deploy_config.py directly." + os.linesep)
    for key in env_vars_to_infra:
        val = os.environ[key]
        fp.write(terraform_variable_template.format(name=key, val=val))
```

Finally, the cloud providers file `providers.tf`:

```python
with open(os.path.join(infra_root, args.component, "providers.tf"), "w") as fp:
    fp.write(terraform_providers_template.format(
        aws_region=os.environ['AWS_DEFAULT_REGION'],
        gcp_project_id=GCP_PROJECT_ID,
    ))
```


# Workflow

We now have a top-level Makefile that wraps the plan and apply commands directly,
and we have an infra-level Makefile with additional commands for managing infrastructure
(plan, apply, destroy).

## Plan

The terraform plan step assembles the various templated terraform files and substitutes
environment variables into them, creating a new version of them with up-to-date values.

The plan step (`make plan-infra`) calls the `build_deploy_config.py` script (detailed above)
to regenerate the terraform files when environment variables are changed.

```
make plan-infra
```

This script will iterate over each cloud infrastructure component in `infra/`, use terraform
to plan the changes it would make to cloud resources, and print a summary of those changes
to the screen.

**The `make plan-infra` command does not change any cloud infra.**

## Deploy

The terraform deploy step makes the changes summarized in the `make plan-infra` step. This
command automates the terraform commands, but still requires interactive "yes" responses
to commands.

## Update

Using the `make plan-infra` command will remake the terraform files using environment variable
values, and will display any changes that will be made to cloud infra. This includes updates to
existing infrastructure.

When you finish deploying infrastructure, store the version of your `environment` file in version
control and tag it as the current deployed infra. This will make it easier to delete infra later.

If you need to rename infra, use the following workflow:

1.  Source the old `environment` file

2.  Destroy the old infra with the old names using:
    
    ```
    make -C infra COMPONENT=buckets destroy
    ```

    Or destroy all infra with the `destroy-all` command:

    ``` 
    make -C infra destroy-all
    ```

3.  Update the environment file with the new names, and source the new `environment` file

4.  Plan the new infra with

    ```
    make plan-infra
    ```

5.  Deploy the new infra with

    ```
    make deploy-infra
    ```

## Destroy

As seen above, infrastructure components can be deleted with the `delete` command in the infra
Makefile, and all infrastructure components can be deleted with the `delete-all` command.

To delete a particular component:

```
make -C infra COMPONENT=buckets destroy
```

To destroy all infra:

```
make -C infra destroy-all
```

