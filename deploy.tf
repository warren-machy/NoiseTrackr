provider "azurerm" {
  features {}
  subscription_id = "a4446539-7abe-4626-ac48-d7025263dbe5"
  client_id       = "369f2e0d-57f2-44f6-a978-7e0d845fe1f7"
  client_secret   = "1Tc8Q~BCsjy~oBKiABvC9ra7uZGdHnblJoW4qdsn"
  tenant_id       = "409d7a11-b871-4827-8e32-43801826897e"
}

resource "azurerm_resource_group" "example" {
  name     = "ForgeAIGroup"
  location = "East US"
}

resource "azurerm_storage_account" "example" {
  name                     = "forgestorageterra"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "example" {
  name                  = "imagefiles"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}

resource "azurerm_container_registry" "example" {
  name                = "forgeacr"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  sku                 = "Basic"
  admin_enabled       = true
}

data "azurerm_container_registry" "example" {
  name                = azurerm_container_registry.example.name
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_service_plan" "example" {
  name                = "forgeAppServicePlanterra"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  os_type  = "Linux"
  sku_name = "B1"
}

resource "azurerm_function_app" "example" {
  name                       = "forgefunctionapp"
  location                   = azurerm_resource_group.example.location
  resource_group_name        = azurerm_resource_group.example.name
  app_service_plan_id        = azurerm_service_plan.example.id
  storage_account_name       = azurerm_storage_account.example.name
  storage_account_access_key = azurerm_storage_account.example.primary_access_key
  version                    = "~3"
  site_config {
    linux_fx_version = "DOCKER|${azurerm_container_registry.example.login_server}/${var.docker_image_name}:${var.docker_image_tag}"
  }
  app_settings = {
    "AzureWebJobsStorage" = azurerm_storage_account.example.primary_connection_string
  }
}

resource "null_resource" "docker_build" {
  provisioner "local-exec" {
    command = "docker build -t ${azurerm_container_registry.example.login_server}/${var.docker_image_name}:${var.docker_image_tag} ."
  }
}

resource "null_resource" "docker_login" {
  provisioner "local-exec" {
    command = "docker login ${azurerm_container_registry.example.login_server} -u ${data.azurerm_container_registry.example.admin_username} -p ${data.azurerm_container_registry.example.admin_password}"
  }
}

resource "null_resource" "docker_push" {
  provisioner "local-exec" {
    command = "docker push ${azurerm_container_registry.example.login_server}/${var.docker_image_name}:${var.docker_image_tag}"
  }

  depends_on = [null_resource.docker_build, null_resource.docker_login]
}

variable "docker_image_name" {
  default = "imagecaptiondockerimage"
}

variable "docker_image_tag" {
  default = "latest"
}
