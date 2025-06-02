# versions.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0" # or any other suitable version
    }
    azapi = {
      source  = "Azure/azapi"
      version = "~> 1.2.0"
    }
  }
}