import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ExemplarToolbarComponent } from './toolbar.component';

import {
  MdcTopAppBarModule,
  MdcButtonModule,
  MdcElevationModule,
  MdcIconModule,
  MdcTypographyModule,
  MdcMenuModule
} from '@angular-mdc/web';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MdcTopAppBarModule,
    MdcButtonModule,
    MdcElevationModule,
    MdcIconModule,
    MdcTypographyModule,
    MdcMenuModule
  ],
  declarations: [ExemplarToolbarComponent],
  exports: [ExemplarToolbarComponent]
})
export class ExemplarToolbarComponentModule { }
