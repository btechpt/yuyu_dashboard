#!/bin/bash

echo "Specify Horizon Location (ex: /etc/horizon): "
read horizon_path
root=`pwd -P`

echo "Removing yuyu Symlink"
rm $horizon_path/openstack_dashboard/dashboards/yuyu
rm $horizon_path/openstack_dashboard/local/enabled/_6100_yuyu.py
rm $horizon_path/openstack_dashboard/local/enabled/_6101_admin_billing_panel_group.py
rm $horizon_path/openstack_dashboard/local/enabled/_6102_admin_billing_overview.py
rm $horizon_path/openstack_dashboard/local/enabled/_6103_admin_billing_price_configuration.py
rm $horizon_path/openstack_dashboard/local/enabled/_6104_admin_billing_setting.py
rm $horizon_path/openstack_dashboard/local/enabled/_6104_admin_billing_setting.py
rm $horizon_path/openstack_dashboard/local/enabled/_6105_admin_billing_projects_invoice.py

rm $horizon_path/openstack_dashboard/local/enabled/_6111_project_billing_panel_group.py
rm $horizon_path/openstack_dashboard/local/enabled/_6112_project_billing_overview.py
rm $horizon_path/openstack_dashboard/local/enabled/_6113_project_billing_usage_cost.py
rm $horizon_path/openstack_dashboard/local/enabled/_6114_project_billing_invoice.py
echo "Yuyu Removal Done"