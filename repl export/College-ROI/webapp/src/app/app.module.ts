import { APP_ID, Inject, NgModule, PLATFORM_ID } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { isPlatformBrowser } from '@angular/common';
import { MdcTypographyModule } from '@angular-mdc/web';

// Angular Universal requires HttpClientModule to be declared at app level
// https://www.thecodecampus.de/blog/angular-universal-xmlhttprequest-not-defined-httpclient/
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { UserInfoModule } from './modules/user-info/user-info.module'
import { AnalysisModule } from './modules/analysis/analysis.module'
import { WelcomeModule } from './modules/welcome/welcome.module'
import { AppComponent } from './app.component';
import { ExemplarToolbarComponentModule } from './components';


@NgModule({
  imports: [
    BrowserModule.withServerTransition({ appId: 'angular-exemplar' }),
    AppRoutingModule,
    AnalysisModule,
    UserInfoModule,
    WelcomeModule,
    HttpClientModule,
    MdcTypographyModule,
    ExemplarToolbarComponentModule
  ],
  declarations: [
    AppComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(@Inject(PLATFORM_ID) private platformId: Object, @Inject(APP_ID) private appId: string) {
    const platform = isPlatformBrowser(platformId) ? 'in the browser' : 'on the server';
    console.log(`Running ${platform} with appId=${appId}`);
  }
}