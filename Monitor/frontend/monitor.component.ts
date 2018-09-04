import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Pattern } from './common/pattern';
import { MonitorService } from "./monitor.service";
import { ImageService } from "./common/image.service";

@Component({
  selector: 'app-monitor',
  templateUrl: './monitor.component.html',
  styleUrls: ['./monitor.component.scss']
})
export class MonitorComponent implements OnInit {


  patterns: Pattern[] = []; // List of patterns loaded from backend
  active: string = 'Dashboard'; //Currently active pattern name
  activePattern = null; //Currently active pattern
  graphLinks: string[] = []; // List of paths to graphs, loaded from backend
  graphs: any[] = []; // Array of graph images to show
  isImageLoading: boolean = false;
  imagesToShow: any[] = [];
  constructor(
    private monitorService: MonitorService,
    private imageService: ImageService
  ) {
  }

  ngOnInit() {
    this.getPatterns();
    this.getGraphLinks('default');
    this.getImageFromService('diskstats_iops-day.png'); // TODO: Remove this
    this.getImageFromService('diskstats_iops/data_data-day.png');
  }

  /** Returns list of patterns from server */
  getPatterns(): void {
    this.monitorService.getPatterns()
      .subscribe(patterns => this.patterns = patterns);
  }

  /** Returns list of image links to use in getImageFromService function. */
  getGraphLinks(category): void {
    this.monitorService.getGraphs(category)
      .subscribe(links => this.graphLinks = links);
  }

  /**
   * Creates image from blob using JS FileReader.
   * @param image - Blob returned from server
   * */
  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imagesToShow.push(reader.result);
    }, false);

    if (image) {
      reader.readAsDataURL(image);
    }
  }

  /**
   * Returns an image based on its path relative to Munin home folder.
   * @param imagePath - Path to an image relative to munin home folder.
   * @note '../' is not supported for security reasons
   * */
  getImageFromService(imagePath: string) {
    this.isImageLoading = true;
    this.imageService.getImage(imagePath).subscribe(data => {
      this.createImageFromBlob(data);
      this.isImageLoading = false;

    }, error => {
      this.isImageLoading = false;
      console.log(error);
    });
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
        this.getGraphLinks(newTabName);
        return;
      }
    }
    this.active = 'Dashboard';
    this.activePattern = null;
    this.getGraphLinks('default');

  }

  setDisplayInterval(): void {
    console.log('Interval changed');
  }

}
