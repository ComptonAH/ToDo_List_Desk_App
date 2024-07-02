import flet as ft
import os


class Task(ft.Row):
    def __init__(self, text: str):
        if not text == "":
            super().__init__()
            self.text_view = ft.Text(text.capitalize(),
                                     width=255,
                                     font_family="RobotoSlab",
                                     weight=ft.FontWeight.W_500,
                                     size=18,
                                     visible=True
                                     )
            self.text_edit = ft.TextField(text.capitalize(),
                                          width=255,
                                          visible=False)
            self.edit_btn = ft.FloatingActionButton(icon=ft.icons.EDIT,
                                                    on_click=self.edit_task,
                                                    elevation=20,
                                                    visible=True)
            self.save_btn = ft.FloatingActionButton(icon=ft.icons.SAVE,
                                                    on_click=self.save_task,
                                                    elevation=20,
                                                    visible=False
                                                    )
            self.controls = [self.text_view,
                             self.text_edit,
                             self.edit_btn,
                             self.save_btn]

    def edit_task(self, e):
        self.text_view.visible = False
        self.text_edit.visible = True
        self.edit_btn.visible = False
        self.save_btn.visible = True
        self.update()

    def save_task(self, e):
        self.text_view.visible = True
        self.text_view.value = self.text_edit.value
        self.text_edit.visible = False
        self.edit_btn.visible = True
        self.save_btn.visible = False
        self.update()


def main(page: ft.Page):
    def add_init_tasks(saved_data):
        for index, task in enumerate(saved_data):
            tasks.controls.append(ft.Row([ft.Checkbox(on_change=show_del_add_icon,
                                                      value=False
                                                      ),
                                          Task(text=task)]))

    def add_task(e):
        task = Task(text=new_txt.value)
        tasks.controls.append(ft.Row([ft.Checkbox(on_change=show_del_add_icon,
                                                  value=False
                                                  ),
                                      task]))
        enter_field.controls[0].controls[0].value = ""
        view.update()

    def show_del_add_icon(e):
        selected = False
        for rows in tasks.controls:
            if rows.controls[0].value:
                selected = True
        if selected:
            enter_field.controls[0].controls[1].visible = False
            enter_field.controls[0].controls[2].visible = True
        else:
            enter_field.controls[0].controls[1].visible = True
            enter_field.controls[0].controls[2].visible = False
        view.update()

    def del_tasks(e):
        index = 0
        while index < len(tasks.controls):
            if tasks.controls[index].controls[0].value:
                tasks.controls.remove(tasks.controls[index])
            else:
                index += 1
        show_del_add_icon(e)

    BG1 = "#FF69B4"
    BG2 = "#FF1493"

    new_txt = ft.TextField(autofocus=True,
                           label="Write stuff to do",
                           width=370,
                           visible=True
                           )
    global tasks
    tasks = ft.Column(auto_scroll=True,
                      scroll=ft.ScrollMode.HIDDEN
                      )

    del_btn = ft.FloatingActionButton(icon=ft.icons.DELETE,
                                      on_click=del_tasks,
                                      elevation=20,
                                      visible=False)

    adding_btn = ft.FloatingActionButton(icon=ft.icons.ADD,
                                         on_click=add_task,
                                         elevation=20,
                                         visible=True)

    enter_field = ft.Column([ft.Row([new_txt, adding_btn, del_btn]),
                             ft.Container(tasks,
                                          bgcolor=BG1,
                                          width=435,
                                          height=390,
                                          border_radius=10,
                                          padding=10,
                                          )
                             ]
                            )

    view = ft.Container(content=enter_field,
                        bgcolor=BG2,
                        width=500,
                        height=500,
                        border_radius=30,
                        padding=ft.padding.only(top=20, left=35)
                        )

    if data.readable():
        init_tasks = []
        for init_row in data.readlines():
            if '\n' in init_row:
                edited_row = init_row[:-1]
                init_tasks.append(edited_row)
            else:
                init_tasks.append(init_row)
        add_init_tasks(init_tasks)

    page.title = "ToDo List"
    page.auto_scroll = True
    page.scroll = ft.ScrollMode.HIDDEN
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)


if __name__ == '__main__':
    if os.path.exists(os.curdir + '/save.txt'):
        data = open('save.txt', 'r+')
    else:
        data = open('save.txt', 'w')
    ft.app(target=main)
    data.close()

    with open('save.txt', 'w') as data:
        new_data = []
        for row in tasks.controls:
            if '\n' in row.controls[1].text_view.value:
                new_data.append(row.controls[1].text_view.value[:-1])
            else:
                new_data.append(row.controls[1].text_view.value)

        for index, data_line in enumerate(new_data):
            if index != len(new_data) - 1:
                data.write(data_line + '\n')
            else:
                data.write(data_line)