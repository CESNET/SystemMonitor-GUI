import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule} from '@angular/router';
import { FormsModule } from '@angular/forms';
import { FilterPipe} from "./common/filter.pipe";

import { MonitorComponent } from "./monitor.component";

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AuthGuard } from 'app/utils/auth.guard';
import { SafePipe, SafePipeModule } from 'app/utils/safe.pipe';
import { HttpClientModule } from '@angular/common/http';

const routes: Routes = [{
  path: 'monitor',
  component: MonitorComponent,
  canActivate: [AuthGuard],
  data: {
    role: 10,
    name: 'Monitor',
    description: 'Server monitoring using Munin',
    icon: 'fa-television',
  },
  children: []
}];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SafePipeModule,
    HttpClientModule,
    RouterModule.forChild(routes),
    NgbModule.forRoot(),
  ],
  declarations: [
    MonitorComponent,
    FilterPipe
  ],
  providers: [
    SafePipe
  ]
})
export class MonitorModule {}
