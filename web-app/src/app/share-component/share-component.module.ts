import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SideNavbarComponent } from './side-navbar/side-navbar.component';
import { MaterialModule } from '../material-module/material-module.module';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';



@NgModule({
  declarations: [
    SideNavbarComponent,
    PageNotFoundComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    MaterialModule,
  ],
  exports: [
    SideNavbarComponent,
    PageNotFoundComponent
  ]
})
export class ShareComponentModule { }
