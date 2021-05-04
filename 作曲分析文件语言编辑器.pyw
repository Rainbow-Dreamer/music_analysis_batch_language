import traceback
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from tkinter import filedialog

function_names = dir() + ['print']
from music_analysis import whole_translate
with open('config.py', encoding='utf-8-sig') as f:
    exec(f.read())


def print(obj):
    root.outputs.insert(END, str(obj))
    root.outputs.insert(END, '\n')
    root.outputs.see(INSERT)


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.minsize(1250, 600)
        self.title('作曲分析文件语言编辑器')
        self.focus_set()
        self.background_color = config_dict['background_color']
        self.foreground_color = config_dict['foreground_color']
        self.active_background_color = config_dict['active_background_color']
        self.day_color, self.night_color = config_dict['day_and_night_colors']
        self.configure(background=self.background_color)
        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton',
                        background=self.background_color,
                        foreground=self.foreground_color,
                        width=10,
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor='none')
        style.configure('TCheckbutton',
                        background=self.background_color,
                        foreground=self.foreground_color,
                        width=12,
                        borderwidth=0,
                        focusthickness=3,
                        focuscolor='none')
        style.configure('TLabel',
                        background=self.background_color,
                        foreground=self.foreground_color)
        style.map('TButton',
                  background=[('active', self.active_background_color)])
        style.map('TCheckbutton',
                  background=[('active', self.active_background_color)])
        self.inputs_text = ttk.Label(self,
                                     text='请在这里输入作曲分析文件语言',
                                     background=self.background_color)
        self.inputs = Text(self,
                           wrap='none',
                           undo=True,
                           autoseparators=True,
                           maxundo=-1)
        self.font_type = config_dict['font_type']
        self.font_size = config_dict['font_size']
        self.inputs.configure(font=(self.font_type, self.font_size))
        self.inputs_text.place(x=0, y=30)
        self.inputs.place(x=0, y=60, width=600, height=500)
        self.inputs.focus_set()
        inputs_v = ttk.Scrollbar(self,
                                 orient="vertical",
                                 command=self.inputs.yview)
        inputs_h = ttk.Scrollbar(self,
                                 orient="horizontal",
                                 command=self.inputs.xview)
        self.inputs.configure(yscrollcommand=inputs_v.set,
                              xscrollcommand=inputs_h.set)
        inputs_v.place(x=600, y=60, height=500)
        inputs_h.place(x=0, y=560, width=600)
        self.outputs_text = ttk.Label(self,
                                      text='在这里显示运行结果',
                                      background=self.background_color)
        self.outputs = Text(self, wrap='none')
        self.outputs.configure(font=(self.font_type, self.font_size))
        self.outputs_text.place(x=600, y=30)
        self.outputs.place(x=614, y=60, width=600, height=500)
        outputs_v = ttk.Scrollbar(self,
                                  orient="vertical",
                                  command=self.outputs.yview)
        outputs_h = ttk.Scrollbar(self,
                                  orient="horizontal",
                                  command=self.outputs.xview)
        self.outputs.configure(yscrollcommand=outputs_v.set,
                               xscrollcommand=outputs_h.set)
        outputs_v.place(x=1200, y=60, height=500)
        outputs_h.place(x=600, y=560, width=600)
        self.run_button = ttk.Button(self, text='运行', command=self.runs)
        self.run_button.place(x=160, y=0)
        self.realtime = IntVar()
        self.realtime.set(1)
        self.realtime_box = ttk.Checkbutton(self,
                                            text='实时运行',
                                            variable=self.realtime,
                                            command=self.check_realtime)
        self.is_realtime = 1
        self.quit = False
        self.auto = IntVar()
        self.auto.set(1)
        self.is_auto = 1
        self.auto_box = ttk.Checkbutton(self,
                                        text='自动补全',
                                        variable=self.auto,
                                        command=self.check_auto)
        self.is_grammar = 1
        self.grammar = IntVar()
        self.grammar.set(1)
        self.grammar_box = ttk.Checkbutton(self,
                                           text='语法高亮',
                                           variable=self.grammar,
                                           command=self.check_grammar)
        self.eachline_character = config_dict['eachline_character']
        self.pairing_symbols = config_dict['pairing_symbols']
        self.wraplines_number = config_dict['wraplines_number']
        self.wraplines_button = ttk.Button(self,
                                           text='自动换行',
                                           command=self.wraplines)
        self.realtime_box.place(x=400, y=0)
        self.auto_box.place(x=500, y=0)
        self.grammar_box.place(x=600, y=0)
        self.wraplines_button.place(x=700, y=0)

        self.outputs_file_button = ttk.Button(self,
                                              text='输出文件',
                                              command=self.outputs_file)
        self.outputs_file_button.place(x=800, y=0)

        self.save_button = ttk.Button(self, text='保存', command=self.save)
        self.save_button.place(x=80, y=0)
        self.pre_input = ''
        self.start = 0
        self.start2 = 0
        self.changed = False
        self.auto_complete_menu = Listbox(self)
        self.auto_complete_menu.bind("<<ListboxSelect>>",
                                     lambda e: self.enter_choose(e))
        self.update()
        self.select_ind = 0
        self.show_select = False
        self.bind('<Up>', lambda e: self.change_select(-1))
        self.bind('<Down>', lambda e: self.change_select(1))
        self.bind('<Left>', self.close_select)
        self.bind('<Right>', self.close_select)
        self.bind('<Return>', lambda e: self.get_current_select(e))
        self.file_top = ttk.Button(self,
                                   text='文件',
                                   command=self.file_top_make_menu)
        #self.file_top.bind(
        #'<Enter>', lambda e: self.file_top.configure(
        #background=self.active_background_color))
        #self.file_top.bind(
        #'<Leave>', lambda e: self.file_top.configure(background=self.
        #background_color))
        #self.file_top.bind('<Button-1>', self.file_top_make_menu)
        self.file_menu = Menu(self,
                              tearoff=0,
                              bg=self.background_color,
                              activebackground=self.active_background_color)
        self.file_menu.add_command(label='打开',
                                   command=self.openfile,
                                   foreground=self.foreground_color)
        self.file_menu.add_command(label='保存',
                                   command=self.save,
                                   foreground=self.foreground_color)
        self.file_menu.add_command(label='设置',
                                   command=self.config_options,
                                   foreground=self.foreground_color)
        self.file_top.place(x=0, y=0)
        self.config_button = ttk.Button(self,
                                        text='设置',
                                        command=self.config_options)
        self.config_button.place(x=320, y=0)
        grammar_highlight = config_dict['grammar_highlight']
        for each in grammar_highlight:
            grammar_highlight[each].sort(key=lambda s: len(s), reverse=True)
        self.grammar_highlight = grammar_highlight
        for each in self.grammar_highlight:
            self.inputs.tag_configure(each, foreground=each)

        self.auto_complete_run()
        self.realtime_run()
        try:
            with open('browse memory.txt') as f:
                self.last_place = f.read()
        except:
            self.last_place = "/"
        self.bg_mode = config_dict['background_mode']
        self.turn_bg_mode = ttk.Button(
            self,
            text='开灯' if self.bg_mode == 'black' else '关灯',
            command=self.change_background_color_mode)
        self.turn_bg_mode.place(x=240, y=0)
        self.change_background_color_mode(turn=False)

        self.menubar = Menu(self,
                            tearoff=False,
                            bg=self.background_color,
                            activebackground=self.active_background_color)
        self.inputs.bind("<Button-3>", lambda x: self.rightKey(x, self.inputs))
        self.first_load_config()

        self.inputs.bind("<Button-3>", lambda x: self.rightKey(x, self.inputs))
        self.first_load_config()
        self.inputs.bind('<Control-w>', self.openfile)
        self.inputs.bind('<Control-s>', self.save)
        self.inputs.bind('<Control-q>', lambda e: self.destroy())
        self.inputs.bind('<Control-r>', lambda e: self.runs())
        self.inputs.bind('<Control-g>',
                         lambda e: self.change_background_color_mode(True))
        self.inputs.bind('<Control-b>', lambda e: self.config_options())
        self.inputs.bind('<Control-MouseWheel>',
                         lambda e: self.change_font_size(e))

        self.config_box_open = False

    def change_font_size(self, e):
        num = e.delta // 120
        self.font_size += num
        if self.font_size < 1:
            self.font_size = 1
        config_dict['font_size'] = self.font_size
        self.inputs.configure(font=(self.font_type, self.font_size))
        self.outputs.configure(font=(self.font_type, self.font_size))
        self.save_config(True)

    def change_background_color_mode(self, turn=True):
        if turn:
            self.bg_mode = 'white' if self.bg_mode == 'black' else 'black'
        if self.bg_mode == 'white':
            self.inputs.configure(bg=self.day_color,
                                  fg='black',
                                  insertbackground='black')
            self.outputs.configure(bg=self.day_color,
                                   fg='black',
                                   insertbackground='black')
            self.bg_mode = 'white'
            self.turn_bg_mode.configure(text='关灯')
        elif self.bg_mode == 'black':
            self.inputs.configure(background=self.night_color,
                                  foreground='white',
                                  insertbackground='white')
            self.outputs.configure(background=self.night_color,
                                   foreground='white',
                                   insertbackground='white')
            self.bg_mode = 'black'
            self.turn_bg_mode.configure(text='开灯')
        if turn:
            config_dict['background_mode'] = self.bg_mode
            self.save_config(True)

    def openfile(self, e=None):
        filename = filedialog.askopenfilename(initialdir=self.last_place,
                                              title="选择文件",
                                              filetype=(("所有文件", "*.*"), ))
        if filename:
            memory = filename[:filename.rindex('/') + 1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place = memory
            try:
                with open(filename, encoding='utf-8-sig',
                          errors='ignore') as f:
                    self.inputs.delete('1.0', END)
                    self.inputs.insert(END, f.read())
                    self.inputs.see(INSERT)
                    self.inputs.mark_set(INSERT, '1.0')
                    if self.is_grammar:
                        self.after(100, self.grammar_highlight_func)
            except:
                self.inputs.delete('1.0', END)
                self.inputs.insert(END, '不是有效的文本文件类型')

    def file_top_make_menu(self):
        self.file_menu.tk_popup(x=self.winfo_pointerx(),
                                y=self.winfo_pointery())

    def wraplines(self):
        N = self.eachline_character
        text = self.outputs.get('1.0', END)
        K = len(text)
        text = ('\n' * self.wraplines_number).join(
            [text[i:i + N] for i in range(0, K, N)])
        self.outputs.delete('1.0', END)
        self.outputs.insert(END, text)

    def first_load_config(self):
        self.get_config_dict = {}

    def close_config_box(self):
        self.config_window.destroy()
        self.config_box_open = False

    def config_options(self):
        if self.config_box_open:
            self.config_window.focus_set()
            return
        self.config_box_open = True
        self.config_window = Toplevel(self, bg=self.background_color)
        self.config_window.minsize(800, 620)
        self.config_window.title('设置')
        self.config_window.protocol("WM_DELETE_WINDOW", self.close_config_box)
        self.get_config_dict = {}
        counter = 0
        for each in config_dict:
            current_label = ttk.Label(self.config_window,
                                      text=each,
                                      background=self.background_color)
            current_entry = ttk.Entry(self.config_window, width=70)
            current_entry.insert(0, str(config_dict[each]))
            current_label.place(x=0, y=counter)
            current_entry.place(x=150, y=counter)
            if each in path_enable_list:
                path_button = ttk.Button(
                    self.config_window,
                    text='更改',
                    command=lambda current_entry=current_entry: self.
                    search_path(current_entry))
                path_button.place(x=650, y=counter)
            counter += 30
            self.get_config_dict[each] = current_entry
        save_button = ttk.Button(self.config_window,
                                 text='保存',
                                 command=self.save_config)
        save_button.place(x=600, y=420)
        self.saved_label = ttk.Label(self.config_window, text='保存成功')
        self.choose_font = ttk.Button(self.config_window,
                                      text='选择字体',
                                      command=self.get_font)
        self.choose_font.place(x=230, y=430)
        self.whole_fonts = list(font.families())
        self.whole_fonts.sort(
            key=lambda x: x if not x.startswith('@') else x[1:])
        self.font_list_bar = ttk.Scrollbar(self.config_window)
        self.font_list_bar.place(x=190, y=490, height=170, anchor=CENTER)
        self.font_list = Listbox(self.config_window,
                                 yscrollcommand=self.font_list_bar.set,
                                 width=25)
        for k in self.whole_fonts:
            self.font_list.insert(END, k)
        self.font_list.place(x=0, y=400)
        self.font_list_bar.config(command=self.font_list.yview)
        current_font_ind = self.whole_fonts.index(self.font_type)
        self.font_list.selection_set(current_font_ind)
        self.font_list.see(current_font_ind)

    def get_font(self):
        self.font_type = self.font_list.get(ACTIVE)
        self.font_size = eval(self.get_config_dict['font_size'].get())
        self.inputs.configure(font=(self.font_type, self.font_size))
        self.outputs.configure(font=(self.font_type, self.font_size))
        self.get_config_dict['font_type'].delete(0, END)
        self.get_config_dict['font_type'].insert(END, self.font_type)
        config_dict['font_type'] = self.font_type
        config_dict['font_size'] = self.font_size
        self.save_config(True)

    def save_config(self, outer=False):
        if not outer:
            for each in config_dict:
                if not isinstance(config_dict[each], str):
                    config_dict[each] = eval(self.get_config_dict[each].get())
                else:
                    config_dict[each] = self.get_config_dict[each].get()
        with open('config.py', 'w', encoding='utf-8-sig') as f:
            f.write(
                f'config_dict = {config_dict}\npath_enable_list = {path_enable_list}'
            )
        if not outer:
            self.saved_label.place(x=600, y=450)
            self.after(300, self.saved_label.place_forget)
        self.reload_config()

    def search_path(self, obj):
        filename = filedialog.askopenfilename(initialdir=self.last_place,
                                              parent=self.config_window,
                                              title="选择文件",
                                              filetype=(("所有文件", "*.*"), ))
        if filename:
            memory = filename[:filename.rindex('/') + 1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place = memory
            obj.delete(0, END)
            obj.insert(END, filename)

    def reload_config(self):
        self.eachline_character = config_dict['eachline_character']
        self.pairing_symbols = config_dict['pairing_symbols']
        self.wraplines_number = config_dict['wraplines_number']
        self.grammar_highlight = config_dict['grammar_highlight']
        for each in self.grammar_highlight:
            self.inputs.tag_configure(each, foreground=each)
        try:
            self.font_size = eval(self.get_config_dict['font_size'].get())
            self.inputs.configure(font=(self.font_type, self.font_size))
            self.outputs.configure(font=(self.font_type, self.font_size))
        except:
            pass

    def save(self, e=None):
        filename = filedialog.asksaveasfilename(initialdir=self.last_place,
                                                title="保存输入文本",
                                                filetype=(("所有文件", "*.*"), ),
                                                defaultextension=".txt")
        if filename:
            memory = filename[:filename.rindex('/') + 1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place = memory
            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.write(self.inputs.get('1.0', END))

    def get_current_select(self, e):
        if self.show_select:
            text = self.auto_complete_menu.get(self.select_ind)
            self.auto_complete_menu.destroy()
            self.show_select = False
            self.inputs.delete('1.0', END)
            self.pre_input = self.pre_input[:self.
                                            start] + text + self.pre_input[
                                                self.start2:]
            self.inputs.insert(END, self.pre_input)
            self.inputs.mark_set(INSERT,
                                 '1.0' + f' + {self.start + len(text)} chars')
            if self.is_realtime:
                self.changed = True
                self.realtime_run()

    def close_select(self, e):
        if self.show_select:
            self.auto_complete_menu.destroy()
            self.show_select = False

    def change_select(self, value):
        if self.show_select:
            sizes = self.auto_complete_menu.size()
            if 0 <= self.select_ind + value < sizes:
                self.auto_complete_menu.selection_set(self.select_ind + value)
                self.auto_complete_menu.selection_clear(self.select_ind)
                self.select_ind += value
                self.auto_complete_menu.see(self.select_ind)
            else:
                if self.select_ind + value >= sizes:
                    self.auto_complete_menu.selection_clear(self.select_ind)
                    self.select_ind = 0
                    self.auto_complete_menu.selection_set(self.select_ind)
                    self.auto_complete_menu.see(self.select_ind)
                else:
                    self.auto_complete_menu.selection_clear(self.select_ind)
                    self.select_ind = sizes - 1
                    self.auto_complete_menu.selection_set(self.select_ind)
                    self.auto_complete_menu.see(self.select_ind)

    def enter_choose(self, e):
        text = self.auto_complete_menu.get(ANCHOR)
        self.auto_complete_menu.destroy()
        self.show_select = False
        self.inputs.delete('1.0', END)
        self.pre_input = self.pre_input[:self.start] + text + self.pre_input[
            self.start2:]
        self.inputs.insert(END, self.pre_input)
        self.inputs.mark_set(INSERT,
                             '1.0' + f' + {self.start + len(text)} chars')
        if self.is_realtime:
            self.changed = True
            self.realtime_run()

    def auto_complete_run(self):
        if not self.is_auto:
            return
        current_text = self.inputs.get('1.0', 'end-1c')
        if current_text != self.pre_input:
            self.changed = True
            is_deleted = len(current_text) < len(self.pre_input)
            self.pre_input = current_text
            self.auto_complete_menu.destroy()
            self.show_select = False
            current_text2 = self.inputs.get('1.0', INSERT)
            if current_text2 and current_text2[-1] not in [' ', '\n']:
                for each in self.pairing_symbols:
                    if current_text2[-1] == each[0] and not is_deleted:
                        self.inputs.insert(INSERT, each[1])
                        self.pre_input = self.inputs.get('1.0', 'end-1c')
                        x, y = self.inputs.index(INSERT).split('.')
                        self.inputs.mark_set(INSERT, f'{x}.{int(y)-1}')
                        break
                else:
                    newline_ind, dot_ind = current_text2.rfind(
                        '\n') + 1, current_text2.rfind('.') + 1
                    start = max(newline_ind, dot_ind)
                    if dot_ind > newline_ind:
                        dot_word_ind = newline_ind
                        if current_text2[dot_word_ind] in ['/', '?']:
                            dot_word_ind += 1
                        current_word = current_text2[dot_word_ind:dot_ind - 1]
                        dot_content = current_text2[dot_ind:].lower()
                        try:
                            current_func = dir(eval(current_word))
                            find_similar = [
                                x for x in current_func
                                if dot_content in x.lower()
                            ]
                            if find_similar:
                                self.start = start
                                self.start2 = start + len(dot_content)
                                self.auto_complete(find_similar)
                        except:
                            pass
                    else:
                        if current_text2[start] in ['/', '?']:
                            start += 1
                        current_word = current_text2[start:].lower()
                        find_similar = [
                            x for x in function_names
                            if current_word in x.lower()
                        ]
                        if find_similar:
                            self.start = start
                            self.start2 = start + len(current_word)
                            self.auto_complete(find_similar)
        else:
            if not self.is_realtime:
                self.changed = False
        self.after(10, self.auto_complete_run)

    def get_input_place(self):
        character = self.inputs.get(INSERT)
        x, y, width, height = self.inputs.bbox(INSERT)
        screen_x = x + (0 if character == '\n' else width)
        screen_y = y + height + 15
        return screen_x, screen_y

    def auto_complete(self, find_similar):
        self.auto_complete_menu = Listbox(self)
        self.auto_complete_menu.bind("<<ListboxSelect>>",
                                     lambda e: self.enter_choose(e))
        places = self.get_input_place()
        for each in find_similar:
            self.auto_complete_menu.insert(END, each)
        self.auto_complete_menu.place(x=places[0], y=places[1])
        self.show_select = True
        self.select_ind = 0
        self.auto_complete_menu.selection_set(0)

    def runs(self):
        if self.is_grammar and self.inputs.edit_modified():
            self.after(100, self.grammar_highlight_func)
        self.outputs.delete('1.0', END)
        text = self.inputs.get('1.0', END)
        print(whole_translate(text))

    def runs_2(self):
        self.inputs.edit_modified(False)
        self.outputs.delete('1.0', END)
        text = self.pre_input
        print(whole_translate(text))

    def grammar_highlight_func(self):
        end_index = self.inputs.index(END)
        for color, texts in self.grammar_highlight.items():
            for i in texts:
                start_index = f"{self.inputs.index(INSERT).split('.')[0]}.0"
                current_last_index = '1.0'
                while self.inputs.compare(start_index, '<', end_index):
                    current_text_index = self.inputs.search(i,
                                                            start_index,
                                                            stopindex=END)
                    if current_text_index:
                        word_length = len(i)
                        x, y = current_text_index.split('.')
                        current_last_index = f"{x}.{int(y)+word_length}"
                        self.inputs.tag_add(color, current_text_index,
                                            current_last_index)
                        start_index = current_last_index
                    else:
                        x, y = current_last_index.split('.')
                        if self.inputs.get(current_last_index) == '\n':
                            x = int(x) + 1
                        y = int(y) + 1
                        current_last_index = f'{x}.{y}'
                        start_index = current_last_index

    def realtime_run(self):
        if self.quit or (not self.is_realtime):
            self.quit = False
            return
        if self.is_grammar and self.inputs.edit_modified():
            self.after(100, self.grammar_highlight_func)
        if self.is_auto:
            if self.changed:
                self.changed = False
                self.runs_2()
        else:
            if self.inputs.edit_modified():
                self.pre_input = self.inputs.get('1.0', END)[:-1]
                self.runs_2()

        self.after(100, self.realtime_run)

    def check_realtime(self):
        value = self.realtime.get()
        if value:
            if not self.is_realtime:
                self.is_realtime = 1
                self.realtime_run()
        else:
            if self.is_realtime:
                self.is_realtime = 0
                self.quit = True

    def check_auto(self):
        self.is_auto = self.auto.get()
        if self.is_auto:
            self.auto_complete_run()
        else:
            self.close_select(1)

    def check_grammar(self):
        self.is_grammar = self.grammar.get()

    def cut(self, editor, event=None):
        editor.event_generate("<<Cut>>")

    def copy(self, editor, event=None):
        editor.event_generate("<<Copy>>")

    def paste(self, editor, event=None):
        editor.event_generate('<<Paste>>')

    def choose_all(self, editor, event=None):
        editor.tag_add(SEL, '1.0', END)
        editor.mark_set(INSERT, END)
        editor.see(INSERT)

    def inputs_undo(self, editor, event=None):
        try:
            editor.edit_undo()
        except:
            pass

    def inputs_redo(self, editor, event=None):
        try:
            editor.edit_redo()
        except:
            pass

    def rightKey(self, event, editor):
        self.menubar.delete(0, END)
        self.menubar.add_command(label='剪切',
                                 command=lambda: self.cut(editor),
                                 foreground=self.foreground_color)
        self.menubar.add_command(label='复制',
                                 command=lambda: self.copy(editor),
                                 foreground=self.foreground_color)
        self.menubar.add_command(label='粘贴',
                                 command=lambda: self.paste(editor),
                                 foreground=self.foreground_color)
        self.menubar.add_command(label='全选',
                                 command=lambda: self.choose_all(editor),
                                 foreground=self.foreground_color)
        self.menubar.add_command(label='撤销',
                                 command=lambda: self.inputs_undo(editor),
                                 foreground=self.foreground_color)
        self.menubar.add_command(label='恢复',
                                 command=lambda: self.inputs_redo(editor),
                                 foreground=self.foreground_color)
        self.menubar.post(event.x_root, event.y_root)

    def outputs_file(self):
        filename = filedialog.asksaveasfilename(initialdir=self.last_place,
                                                title="保存生成的作曲分析内容",
                                                filetype=(("所有文件", "*.*"), ),
                                                defaultextension=".txt")
        if filename:
            memory = filename[:filename.rindex('/') + 1]
            with open('browse memory.txt', 'w') as f:
                f.write(memory)
            self.last_place = memory
            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.write(self.outputs.get('1.0', END))


root = Root()
root.mainloop()
