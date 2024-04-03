import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SupportTicketRoutingModule } from './support-ticket-routing.module';
import { SupportTicketListComponent } from './support-ticket-list/support-ticket-list.component';
import { MaterialModule } from '../../material-module/material-module.module';
import { ReplyDialogComponent, SupportTicketDetailComponent } from './support-ticket-detail/support-ticket-detail.component';
import { SupportTicketCreateComponent } from './support-ticket-create/support-ticket-create.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    SupportTicketListComponent,
    SupportTicketDetailComponent,
    SupportTicketCreateComponent,
    ReplyDialogComponent
  ],
  imports: [
    CommonModule,
    SupportTicketRoutingModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
  ]
})
export class SupportTicketModule { }
