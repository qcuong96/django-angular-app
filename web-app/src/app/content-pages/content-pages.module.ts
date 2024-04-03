import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ContentPagesRoutingModule } from './content-pages-routing.module';
import { ContentPagesComponent } from './content-pages.component';
import { MaterialModule } from '../material-module/material-module.module';
import { ShareComponentModule } from '../share-component/share-component.module';


@NgModule({
  declarations: [
    ContentPagesComponent
  ],
  imports: [
    CommonModule,
    ContentPagesRoutingModule,
    MaterialModule,
    ShareComponentModule,
  ]
})
export class ContentPagesModule { }
