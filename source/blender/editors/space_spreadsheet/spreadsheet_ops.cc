/* SPDX-FileCopyrightText: 2023 Blender Authors
 *
 * SPDX-License-Identifier: GPL-2.0-or-later */

#include "DNA_space_types.h"

#include "ED_screen.hh"

#include "BLI_listbase.h"

#include "BKE_context.hh"

#include "RNA_access.hh"
#include "RNA_define.hh"

#include "WM_api.hh"
#include "WM_types.hh"

#include "spreadsheet_intern.hh"
#include "spreadsheet_row_filter.hh"

namespace blender::ed::spreadsheet {

static wmOperatorStatus row_filter_add_exec(bContext *C, wmOperator * /*op*/)
{
  SpaceSpreadsheet *sspreadsheet = CTX_wm_space_spreadsheet(C);

  SpreadsheetRowFilter *row_filter = spreadsheet_row_filter_new();
  BLI_addtail(&sspreadsheet->row_filters, row_filter);

  WM_event_add_notifier(C, NC_SPACE | ND_SPACE_SPREADSHEET, sspreadsheet);

  return OPERATOR_FINISHED;
}

static void SPREADSHEET_OT_add_row_filter_rule(wmOperatorType *ot)
{
  ot->name = "Add Row Filter";
  ot->description = "Add a filter to remove rows from the displayed data";
  ot->idname = "SPREADSHEET_OT_add_row_filter_rule";

  ot->exec = row_filter_add_exec;
  ot->poll = ED_operator_spreadsheet_active;

  ot->flag = OPTYPE_REGISTER | OPTYPE_UNDO;
}

static wmOperatorStatus row_filter_remove_exec(bContext *C, wmOperator *op)
{
  SpaceSpreadsheet *sspreadsheet = CTX_wm_space_spreadsheet(C);

  SpreadsheetRowFilter *row_filter = (SpreadsheetRowFilter *)BLI_findlink(
      &sspreadsheet->row_filters, RNA_int_get(op->ptr, "index"));
  if (row_filter == nullptr) {
    return OPERATOR_CANCELLED;
  }

  BLI_remlink(&sspreadsheet->row_filters, row_filter);
  spreadsheet_row_filter_free(row_filter);

  WM_event_add_notifier(C, NC_SPACE | ND_SPACE_SPREADSHEET, sspreadsheet);

  return OPERATOR_FINISHED;
}

static void SPREADSHEET_OT_remove_row_filter_rule(wmOperatorType *ot)
{
  ot->name = "Remove Row Filter";
  ot->description = "Remove a row filter from the rules";
  ot->idname = "SPREADSHEET_OT_remove_row_filter_rule";

  ot->exec = row_filter_remove_exec;
  ot->poll = ED_operator_spreadsheet_active;

  ot->flag = OPTYPE_REGISTER | OPTYPE_UNDO;

  RNA_def_int(ot->srna, "index", 0, 0, INT_MAX, "Index", "", 0, INT_MAX);
}

static wmOperatorStatus select_component_domain_invoke(bContext *C,
                                                       wmOperator *op,
                                                       const wmEvent * /*event*/)
{
  const auto component_type = bke::GeometryComponent::Type(RNA_int_get(op->ptr, "component_type"));
  bke::AttrDomain domain = bke::AttrDomain(RNA_int_get(op->ptr, "attribute_domain_type"));

  SpaceSpreadsheet *sspreadsheet = CTX_wm_space_spreadsheet(C);
  sspreadsheet->geometry_component_type = uint8_t(component_type);
  sspreadsheet->attribute_domain = uint8_t(domain);

  /* Refresh header and main region. */
  WM_main_add_notifier(NC_SPACE | ND_SPACE_SPREADSHEET, nullptr);

  return OPERATOR_FINISHED;
}

static void SPREADSHEET_OT_change_spreadsheet_data_source(wmOperatorType *ot)
{
  ot->name = "Change Visible Data Source";
  ot->description = "Change visible data source in the spreadsheet";
  ot->idname = "SPREADSHEET_OT_change_spreadsheet_data_source";

  ot->invoke = select_component_domain_invoke;
  ot->poll = ED_operator_spreadsheet_active;

  RNA_def_int(ot->srna, "component_type", 0, 0, INT16_MAX, "Component Type", "", 0, INT16_MAX);
  RNA_def_int(ot->srna,
              "attribute_domain_type",
              0,
              0,
              INT16_MAX,
              "Attribute Domain Type",
              "",
              0,
              INT16_MAX);

  ot->flag = OPTYPE_INTERNAL;
}

void spreadsheet_operatortypes()
{
  WM_operatortype_append(SPREADSHEET_OT_add_row_filter_rule);
  WM_operatortype_append(SPREADSHEET_OT_remove_row_filter_rule);
  WM_operatortype_append(SPREADSHEET_OT_change_spreadsheet_data_source);
}

}  // namespace blender::ed::spreadsheet
