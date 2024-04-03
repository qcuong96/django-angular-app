import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PageNotFoundComponent } from './share-component/page-not-found/page-not-found.component';
import { AuthenticationGuard } from './core/guard/authentication.guard';

const routes: Routes = [
  {
    path: '',
    canActivate: [AuthenticationGuard],
    loadChildren: () => import("./content-pages/content-pages.module").then(m => m.ContentPagesModule)
  },
  {
    path: 'authentication',
    loadChildren: () => import('./sign-user/sign-user.module')
      .then(m => m.SignUserModule),
  },
  { path: '**', component: PageNotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
