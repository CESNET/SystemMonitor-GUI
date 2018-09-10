import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Pattern } from './common/pattern';
import { Image } from './common/image';
import { MonitorService } from "./monitor.service";
import { ImageService } from "./common/image.service";

import { FilterPipe } from "./common/filter.pipe";

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
  isImageLoading: boolean = false;
  imagesToShow: Image[] = []; // Array of graph images
  start: number = 0; // Index from imagesToShow to start displaying graphs from
  max: number = 18; // How many graphs should be on a page. Switched back to 18 after switching a tab
  loadMoreStep: number = 6; // How many graphs should load when "Load more" button is pressed
  searchText: string;
  selectedPattern: string;
  localLinks: string[] = [];
  localLinksLoaded: boolean = true;
  displayInterval: string = 'default'; // Value of interval dropdown
  searchInterval: string = 'all';

  graphToAdd: string;

  graphBuffer: string[] = [];

  constructor(
    private monitorService: MonitorService,
    private imageService: ImageService
  ) {
  }

  ngOnInit() {
    this.getPatterns();
    this.getGraphLinks('default');
  }

  ngOnDestroy() {
    this.saveGraphs();
  }
  @HostListener('window:beforeunload', ['$event'])
  saveOnUnload($event: any) {
    this.saveGraphs();
  }

  /** Returns list of patterns from server */
  getPatterns(): void {
    this.monitorService.getPatterns()
      .subscribe(patterns => this.patterns = patterns);
  }

  /** Simplified version of getGraphLinks, to use on getting dropdown options for "Add graph" form */
  getFormLinks(category): void {
    this.localLinksLoaded = false;
    this.localLinks = [];
    let intervals = [];
    if (this.searchInterval == 'all') {
      intervals = ['day', 'week', 'month', 'year']
    }
    else {
      intervals = [this.searchInterval];
    }
    this.monitorService.getGraphsWithIntervals(category, intervals)
      .subscribe(links => this.localLinks = links, err => console.error(err), () => this.localLinksLoaded = true);
  }


  /** Returns list of image links to use in getImageFromService function. */
  getGraphLinks(category): void {
    this.monitorService.getGraphs(category)
      .subscribe(links => this.graphLinks = links, err => console.error(err), () => this.loadImages(0));
  }

  getFilteredGraphLinks(category: string, intervals: string[]): void {
    this.monitorService.getGraphsWithIntervals(category, intervals)
      .subscribe(links => this.graphLinks = links, err => console.error(err), () => this.loadImages(0));
  }

  /**
   * Combines together functions for getting graph names and function for getting images.
   * @param startAt - start at this index from graphLinks
   */
  loadImages(startAt: number): void {
    let i = 0;
    for (let image in this.graphLinks) {
      // Are we over index, on which we want to start at?
      if (i >= startAt) {
        this.getImageFromService(this.graphLinks[image]);
      }
      i++;
      // We are over limit, end.
      if (i >= this.max) {
        break;
      }
    }
    this.isImageLoading = false;
  }

  /**
   * Creates image from blob using JS FileReader and adds it into imagesToShow variable.
   * @param image - Blob returned from server
   * @param filename - Name of image file
   */
  createImageFromBlob(image: Blob, filename: string) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
      this.imagesToShow.push({filename: filename, image: reader.result});
    }, false);

    if (image) {
      reader.readAsDataURL(image);
    }
  }

  /**
   * Returns an image based on its path relative to Munin home folder.
   * @param imagePath - Path to an image relative to munin home folder.
   * @note '../' is not supported for security reasons
   */
  getImageFromService(imagePath: string) {
    this.imageService.getImage(imagePath).subscribe(data => {
      this.createImageFromBlob(data, imagePath);

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
    // Remove previously loaded images
    this.imagesToShow = [];
    this.max = 18;

    // Check if selected pattern is valid
    for(let pattern of this.patterns) {
      if(pattern['title'] === newTabName) {
        // Pattern is valid, load new images
        this.isImageLoading = true;
        this.active = newTabName;
        this.activePattern = pattern;
        this.setDisplayInterval(); // To keep set interval
        // Save user graphs and empty buffer
        this.saveGraphs();
        return;
      }
    }
    // Pattern is not valid, load dashboard
    this.active = 'Dashboard';
    this.activePattern = null;
    this.displayInterval = 'default';
    this.getGraphLinks('default');



  }

  /** Increase max number of images and load new graphs */
  loadMore(): void {
    this.max += this.loadMoreStep;
    this.loadImages(this.max - this.loadMoreStep);

  }
  /** Change interval of selected graphs (on dashboard) or on all graphs (outside of dashboard) */
  setDisplayInterval(): void {
    // Filter all loaded graphs
    if (this.active !== 'Dashboard') {
      this.graphLinks = [];
      this.imagesToShow = [];
      if (this.displayInterval == 'all' || this.displayInterval == 'default') {
        this.getGraphLinks(this.active);
      }
      else {
        this.getFilteredGraphLinks(this.active, [this.displayInterval]);
      }

    }
    // Update user's database values, change only selected graphs
    else {
      // TODO
    }

  }

  addGraph(graphName: string) {
    this.getImageFromService(graphName);
    this.graphBuffer.push(graphName);
  }

  removeGraph(graphName: string) {
    // Remove from buffer
    for (let graph of this.graphBuffer) {
      if (graph == graphName) {
        let index = this.graphBuffer.indexOf(graphName, 0);

        if (index > -1) {
          this.graphBuffer.splice(index, 1);
          // Removed graph from buffer, save buffer and reload images
          console.log('Graph buffer after removal');
          console.log(this.graphBuffer);
          this.saveGraphs();
          let i = 0;
          for (let image of this.imagesToShow) {
            if (image['filename'] == graphName) {
              this.imagesToShow.splice(i, 1);
            }
            i++;
          }
          // Graph was in buffer, no need to remove it from server
          return;
        }
      }
    }

    // Remove from server
    this.monitorService.removeGraph(graphName)
      .subscribe(res => console.log(res), err => console.error(err));

    // Reload images
    this.saveGraphs();
    this.imagesToShow = [];
    this.getGraphLinks('default');
  }

  /** Add graph to users list of graphs */
  saveGraphs(): void {
    if( this.graphBuffer != []) {
      this.monitorService.addUserGraph(this.graphBuffer)
        .subscribe(res => console.log(res),
            err => console.error(err),
            () => this.graphBuffer = []);
    }

  }

}
