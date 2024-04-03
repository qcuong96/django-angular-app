import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { SupportTicketCreateComponent } from '../support-ticket-create/support-ticket-create.component';
import { SupportTicketServices } from '../../../core/api-services/support-ticket-services.service copy';


@Component({
  selector: 'app-support-ticket-list',
  templateUrl: './support-ticket-list.component.html',
  styleUrl: './support-ticket-list.component.scss'
})
export class SupportTicketListComponent implements OnInit {
  isCreateable = false;
  tableData: any;
  totalPage = 1;
  currentPage = 1;
  totalRecord = 0;
  currentPerPage = 10;
  columnsToDisplay = ['id', 'name', 'priority', 'category', 'status', 'update_time', 'actions'];

  constructor(
    public dialog: MatDialog,
    private supportTicketServices: SupportTicketServices
  ) { }

  async ngOnInit() {
    this.isCreateable = localStorage.getItem('is_employee') === 'false';
    let data = await this.supportTicketServices.getListSupportTicket();
    if (data.error) {
      alert(data.error);
      return;
    }

    let supportTicketList = data.results;
    this.tableData = this.processTableData(supportTicketList);
    this.totalRecord = data.count;
    this.totalPage = Math.ceil(this.totalRecord / this.currentPerPage);
  }

  async getData(){
    let data = await this.supportTicketServices.getListSupportTicket(this.currentPage);
    if (data.error) {
      alert(data.error);
      return;
    }

    let supportTicketList = data.results;
    this.tableData = this.processTableData(supportTicketList);
  }

  processTableData(data: any) {
    return data.map((item: any) => {
      return {
        id: item.id,
        name: item.name,
        description: item.description,
        priority: item.priority,
        category: item.category,
        status: item.status,
        update_time: item.update_time
      }
    })
  }

  selectPerPage(event: any) {
    console.log(event);
  }

  async back() {
    this.currentPage--;
    await this.getData();
  }

  async next() {
    this.currentPage++;
    await this.getData();
  }

  createTicket() {
    this.dialog.open(SupportTicketCreateComponent, {});

    // reload ng oninit when close dialog
    this.dialog.afterAllClosed.subscribe(() => {
      this.ngOnInit();
    });
  }

}
