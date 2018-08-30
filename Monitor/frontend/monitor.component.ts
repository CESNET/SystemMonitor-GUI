import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Pattern } from './common/pattern';
import { MonitorService } from "./monitor.service";

@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit {

  patterns: Pattern[];
  active: string = 'Dashboard';
  activePattern = null;
  graphLinks: string[] = [];
  constructor(private monitorService: MonitorService) {
  }

  ngOnInit() {
    this.getPatterns();
  }

  getPatterns(): void {
    this.monitorService.getPatterns()
      .subscribe(patterns => this.patterns = patterns);
  }

  /**
   * Switch active tab to a new tab name.
   * If new tab name is invalid, Dashboard is used.
   * @param newTabName - title of a tab you want to switch to
   */
  switchTab(newTabName: string): void {
    for(let pattern of this.patterns) {
      if(pattern['title'] === newTabName) {
        this.active = newTabName;
        this.activePattern = pattern;
        return;
      }
    }
    this.active = 'Dashboard';
    this.activePattern = null;

  }

}
