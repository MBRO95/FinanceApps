import { NgModule } from '@angular/core';
import { Routes, RouterModule, PreloadAllModules } from '@angular/router';
import { UserInfoComponent } from './modules/user-info/user-info.component';
import { AnalysisComponent } from './modules/analysis/analysis.component';
import { WelcomeComponent } from './modules/welcome/welcome.component';
import { CalculatorService } from './services/calculator.service';

const routes: Routes = [
  {
    path: 'welcome',
    component: WelcomeComponent
  },
  {
    path: 'start',
    component: UserInfoComponent
  },
  {
    path: 'result',
    component: AnalysisComponent,
    resolve: {
      cres: CalculatorService
    }
  },
  {
    path: '',
    redirectTo: 'welcome',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule],
  providers: [CalculatorService]
})
export class AppRoutingModule { }
