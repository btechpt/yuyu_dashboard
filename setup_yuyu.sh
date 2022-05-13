#!/bin/bash

echo "Specify Horizon Location (ex: /etc/horizon): "
read horizon_path
root=`pwd -P`

echo "Creating Symlink"
ln -sf $root/yuyu $horizon_path/openstack_dashboard/dashboards
ln -sf $root/yuyu/local/enabled/_6100_yuyu.py $horizon_path/openstack_dashboard/local/enabled/_6100_yuyu.py
ln -sf $root/yuyu/local/enabled/_6101_admin_billing_panel_group.py $horizon_path/openstack_dashboard/local/enabled/_6101_admin_billing_panel_group.py
ln -sf $root/yuyu/local/enabled/_6102_admin_billing_overview.py $horizon_path/openstack_dashboard/local/enabled/_6102_admin_billing_overview.py
ln -sf $root/yuyu/local/enabled/_6103_admin_billing_price_configuration.py $horizon_path/openstack_dashboard/local/enabled/_6103_admin_billing_price_configuration.py
ln -sf $root/yuyu/local/enabled/_6104_admin_billing_setting.py $horizon_path/openstack_dashboard/local/enabled/_6104_admin_billing_setting.py
ln -sf $root/yuyu/local/enabled/_6104_admin_billing_setting.py $horizon_path/openstack_dashboard/local/enabled/_6104_admin_billing_setting.py
ln -sf $root/yuyu/local/enabled/_6105_admin_billing_projects_invoice.py $horizon_path/openstack_dashboard/local/enabled/_6105_admin_billing_projects_invoice.py

ln -sf $root/yuyu/local/enabled/_6111_project_billing_panel_group.py $horizon_path/openstack_dashboard/local/enabled/_6111_project_billing_panel_group.py
ln -sf $root/yuyu/local/enabled/_6112_project_billing_overview.py $horizon_path/openstack_dashboard/local/enabled/_6112_project_billing_overview.py
ln -sf $root/yuyu/local/enabled/_6113_project_billing_usage_cost.py $horizon_path/openstack_dashboard/local/enabled/_6113_project_billing_usage_cost.py
ln -sf $root/yuyu/local/enabled/_6114_project_billing_invoice.py $horizon_path/openstack_dashboard/local/enabled/_6114_project_billing_invoice.py

echo "Symlink Creation Done"
echo "Now you can configure and yuyu dashboard"