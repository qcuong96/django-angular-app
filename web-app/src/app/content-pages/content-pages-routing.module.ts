import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ContentPagesComponent } from './content-pages.component';

const routes: Routes = [
  {
    path: '',
    component: ContentPagesComponent,
    children: [
      {
        path: 'support-ticket',
        loadChildren: () => import("./support-ticket/support-ticket.module").then(m => m.SupportTicketModule)
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ContentPagesRoutingModule { }
