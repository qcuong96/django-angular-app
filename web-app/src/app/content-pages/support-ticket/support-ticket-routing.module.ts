import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SupportTicketListComponent } from './support-ticket-list/support-ticket-list.component';
import { SupportTicketDetailComponent } from './support-ticket-detail/support-ticket-detail.component';

const routes: Routes = [
  {
    path: '',
    children: [
      {
        path: 'list',
        component: SupportTicketListComponent
      },
      {
        path: ':id',
        component: SupportTicketDetailComponent
      },
      { path: '', redirectTo: 'list', pathMatch: 'full' }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SupportTicketRoutingModule { }
