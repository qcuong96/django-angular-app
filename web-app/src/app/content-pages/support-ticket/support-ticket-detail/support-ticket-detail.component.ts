import { Component, Inject, OnInit } from '@angular/core';
import { SupportTicketServices } from '../../../core/api-services/support-ticket-services.service copy';
import { ActivatedRoute } from '@angular/router';
import { MAT_DIALOG_DATA, MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FormControl, Validators } from '@angular/forms';


@Component({
  selector: 'app-support-ticket-detail',
  templateUrl: './support-ticket-detail.component.html',
  styleUrl: './support-ticket-detail.component.scss'
})
export class SupportTicketDetailComponent implements OnInit {
  ticket: any;
  userId: any;
  isDeleteable: boolean = false;
  isRepliable: boolean = false;
  isEmployee: boolean = false;
  editable: boolean = true;
  support_ticket_id: any;

  constructor(
    public dialog: MatDialog,
    private route: ActivatedRoute,
    private supportTicketServices: SupportTicketServices,
  ) {
    this.support_ticket_id = this.route.snapshot.paramMap.get('id');
  }

  async ngOnInit() {
    this.userId = localStorage.getItem('user_id');
    this.isEmployee = localStorage.getItem('is_employee') === 'true';
    let data : any = await this.supportTicketServices.getDetailSupportTicket(this.support_ticket_id);
    
    if (data.error) {
      alert(data.error);
      return;
    }
    
    this.ticket = data;
    this.updateStatus();
    let ticket_create_time = new Date(this.ticket.create_time);
    this.editable = this.ticket.status === 'NEW' && ((new Date()).getTime() - ticket_create_time.getTime()) / (1000 * 60 * 60) <= 1;
  }

  private updateStatus() {
    this.isRepliable = (this.ticket.reporter === localStorage.getItem('username') || this.ticket.supporter === localStorage.getItem('username')) && !['DONE', 'DELETE'].includes(this.ticket.status);
    this.isDeleteable = (this.ticket.reporter === localStorage.getItem('username') && !['DONE', 'DELETE'].includes(this.ticket.status));
  }

  async assign() {
    if (!this.ticket.supporter && this.isEmployee) {
      let data = await this.supportTicketServices.assignSupporter(this.support_ticket_id, localStorage.getItem('user_id') ?? '');
      if (data.error) {
        alert(data.error);
        return;
      }

      this.ticket.supporter = localStorage.getItem('username');
      this.updateStatus();
    }
  }

  async reply() {
    const dialogRef = this.dialog.open(ReplyDialogComponent, {
      data: {support_ticket_id: this.support_ticket_id,},
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      this.ticket.replies.push(result);
    });
  }
  async edit() {}
  async delete() {
    let data = await this.supportTicketServices.deleteSupportTicket(this.support_ticket_id);
    if (data.error) {
      alert(data.error);
      return;
    }
    this.ticket.status = 'DELETE';
    this.updateStatus();

  }
  async close() {
    let data = await this.supportTicketServices.closeSupportTicket(this.support_ticket_id);
    if (data.error) {
      alert(data.error);
      return;
    }
    this.ticket.status = 'DONE';
    this.updateStatus();
  }

  getClass(replyReplier: number): string {
    return replyReplier == this.userId ? 'odd' : 'even';
  }
}


@Component({
  selector: 'app-reply-dialog',
  templateUrl: './reply-dialog.component.html',
  styleUrl: './reply-dialog.component.scss'
})
export class ReplyDialogComponent {
  replyContent = new FormControl('', [Validators.required, Validators.pattern(/\S/)]);

  constructor(
    public dialogRef: MatDialogRef<SupportTicketDetailComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
    private supportTicketServices: SupportTicketServices,
  ) {}

  async submit(){
    if (this.replyContent.valid) {
      const trimmedContent = this.replyContent.value?.trim();
  
      let _data = await this.supportTicketServices.createReply(this.data.support_ticket_id, {content: trimmedContent});
      if (_data.error) {
        alert(_data.error);
        return;
      }

      this.dialogRef.close(_data);
    }
  }

  close() {
    this.dialogRef.close();
  }
}