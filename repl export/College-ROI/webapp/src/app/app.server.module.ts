import { NgModule } from '@angular/core';
import { ServerModule } from '@angular/platform-server';
import { ModuleMapLoaderModule } from '@nguniversal/module-map-ngfactory-loader';
import { MdcTypographyModule } from '@angular-mdc/web';

import { AppModule } from './app.module';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ExemplarToolbarComponentModule } from './components';

@NgModule({
  imports: [
    AppModule,
    ServerModule,
    ModuleMapLoaderModule,
    AppRoutingModule,
    MdcTypographyModule,
    ExemplarToolbarComponentModule
  ],
  bootstrap: [AppComponent]
})
export class AppServerModule { }