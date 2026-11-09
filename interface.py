# Interface gráfica da aplicação
# Responsabilidade: consumir os dados através dos métodos CRUD da classe Usuario.

import re
import tkinter as tk
from tkinter import ttk, messagebox

from banco import criar_banco
from usuario import Usuario

COR_FUNDO = '#f4f6f8'
COR_CARD = '#ffffff'
COR_TEXTO = '#202124'
COR_DESTAQUE = '#247bd2'
SENHA_MINIMA = 5


REGEX_EMAIL = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def email_valido(email):
    return REGEX_EMAIL.match(email) is not None


class Aplicacao:
    def __init__(self, root):
        self.root = root

        self.root.title('Cadastro de Usuários')
        self.root.geometry('760x650')
        self.root.minsize(680, 520)
        self.root.configure(bg=COR_FUNDO)

        self.criar_interface()
        self.listar_usuarios()

    def criar_interface(self):
        tk.Label(
            self.root,
            text='Cadastro de Usuários',
            font=('Segoe UI', 22, 'bold'),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack(pady=(20, 5))

        tk.Label(
            self.root,
            text='Gerenciador de usuários em janela única',
            font=('Segoe UI', 10),
            bg=COR_FUNDO,
            fg='#5f6368'
        ).pack(pady=(0, 5))

        self.criar_formulario()
        self.criar_lista()

    def criar_formulario(self):
        frame = tk.Frame(self.root, bg=COR_CARD, bd=1, relief='solid')
        frame.pack(fill='x', padx=25, pady=5)

        for coluna, texto in enumerate(('Nome', 'E-mail', 'Senha')):
            tk.Label(
                frame,
                text=texto,
                bg=COR_CARD,
                fg='#333',
                font=('Segoe UI', 10, 'bold')
            ).grid(row=0, column=coluna, padx=15, pady=(15, 5), sticky='w')

        self.entry_nome = ttk.Entry(frame, width=28)
        self.entry_email = ttk.Entry(frame, width=28)
        self.entry_senha = ttk.Entry(frame, width=28, show='*')

        for campo in (self.entry_nome, self.entry_email, self.entry_senha):
            campo.bind('<Return>', lambda event: self.cadastrar())

        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 15))
        self.entry_email.grid(row=1, column=1, padx=15, pady=(0, 15))
        self.entry_senha.grid(row=1, column=2, padx=15, pady=(0, 15))

        self.btn_cadastrar = ttk.Button(
            frame,
            text='Cadastrar',
            command=self.cadastrar
        )
        self.btn_cadastrar.grid(row=1, column=3, padx=(5, 15), pady=(0, 15))

        # Redistribui o espaço extra quando a janela é redimensionada
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

    def criar_lista(self):
        tk.Label(
            self.root,
            text='Usuários cadastrados',
            font=('Segoe UI', 14, 'bold'),
            bg=COR_FUNDO,
            fg=COR_TEXTO
        ).pack(anchor='w', padx=25, pady=(20, 8))

        container = tk.Frame(self.root, bg=COR_FUNDO)
        container.pack(fill='both', expand=True, padx=25, pady=(0, 20))

        # Canvas: o Frame sozinho não oferece rolagem vertical
        self.canvas = tk.Canvas(container, bg=COR_FUNDO, highlightthickness=0)

        scrollbar = ttk.Scrollbar(
            container,
            orient='vertical',
            command=self.canvas.yview
        )

        # Frame que receberá os cards
        self.cards_frame = tk.Frame(self.canvas, bg=COR_FUNDO)

        # Atualiza a região rolável quando o tamanho dos cards muda
        self.cards_frame.bind(
            '<Configure>',
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor='nw'
        )

        # Os cards acompanham a largura disponível
        self.canvas.bind(
            '<Configure>',
            lambda event: self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    # ---------- validações ----------
    def validar(self, nome, email, senha):
        if not nome or not email or not senha:
            messagebox.showwarning('Atenção!', 'Preencha nome, e-mail e senha.')
            return False

        if not email_valido(email):
            messagebox.showwarning('Atenção!', 'Digite um e-mail válido.')
            return False

        if len(senha) < SENHA_MINIMA:
            messagebox.showwarning(
                'Atenção!',
                f'A senha deve possuir pelo menos {SENHA_MINIMA} caracteres.'
            )
            return False

        return True

    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_nome.focus()

    # ---------- cadastro ----------
    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get()

        if not self.validar(nome, email, senha):
            return

        usuario = Usuario(nome, email, senha)
        sucesso, mensagem = usuario.salvar()

        if sucesso:
            messagebox.showinfo('Sucesso!', mensagem)
            self.limpar_formulario()
            self.listar_usuarios()
        else:
            messagebox.showerror('Erro!', mensagem)

    # ---------- listagem ----------
    def listar_usuarios(self):
        # Remove os cards atuais antes de recriar a lista
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        usuarios = Usuario.listar()

        if not usuarios:
            tk.Label(
                self.cards_frame,
                text='Nenhum usuário cadastrado!',
                font=('Segoe UI', 11),
                bg=COR_FUNDO,
                fg='#777'
            ).pack(pady=30)
            return

        for usuario in usuarios:
            self.criar_card(usuario)

    def criar_card(self, usuario):
        card = tk.Frame(self.cards_frame, bg=COR_CARD, bd=1, relief='solid')
        card.pack(fill='x', pady=5)

        informacoes = tk.Frame(card, bg=COR_CARD)
        informacoes.pack(side='left', fill='x', expand=True, padx=10, pady=10)

        tk.Label(
            informacoes,
            text=usuario['nome'],
            font=('Segoe UI', 12, 'bold'),
            bg=COR_CARD,
            fg=COR_DESTAQUE
        ).pack(anchor='w')

        tk.Label(
            informacoes,
            text=usuario['email'],
            font=('Segoe UI', 10),
            bg=COR_CARD,
            fg='#5f6368'
        ).pack(anchor='w', pady=(3, 0))

        botoes = tk.Frame(card, bg=COR_CARD)
        botoes.pack(side='right', padx=15, pady=12)

        ttk.Button(
            botoes,
            text='Atualizar',
            command=lambda u=usuario: self.abrir_edicao(u)
        ).pack(side='left', padx=3)

        ttk.Button(
            botoes,
            text='Excluir',
            command=lambda u=usuario: self.excluir(u['id'])
        ).pack(side='left', padx=3)

    # ---------- exclusão ----------
    def excluir(self, id_usuario):
        resposta = messagebox.askyesno(
            'Confirmar exclusão',
            'Deseja realmente excluir este usuário?'
        )

        if not resposta:
            return

        sucesso, mensagem = Usuario.excluir(id_usuario)

        if sucesso:
            messagebox.showinfo('Sucesso', mensagem)
            self.listar_usuarios()
        else:
            messagebox.showerror('Erro', mensagem)

    # ---------- edição ----------
    def abrir_edicao(self, usuario):
        janela = tk.Toplevel(self.root)
        janela.title('Atualizar Usuário')
        janela.geometry('400x340')
        janela.resizable(False, False)
        janela.transient(self.root)
        janela.grab_set()

        frame = tk.Frame(janela, padx=25, pady=20)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text='Nome', font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        entry_nome = ttk.Entry(frame)
        entry_nome.pack(fill='x', pady=(5, 15))
        entry_nome.insert(0, usuario['nome'])

        tk.Label(frame, text='E-mail', font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        entry_email = ttk.Entry(frame)
        entry_email.pack(fill='x', pady=(5, 15))
        entry_email.insert(0, usuario['email'])

        tk.Label(
            frame,
            text='Nova senha (deixe em branco para manter)',
            font=('Segoe UI', 11, 'bold')
        ).pack(anchor='w')
        entry_senha = ttk.Entry(frame, show='*')
        entry_senha.pack(fill='x', pady=(5, 20))

        def salvar_alteracao():
            nome = entry_nome.get().strip()
            email = entry_email.get().strip()
            senha = entry_senha.get()

            if not nome or not email:
                messagebox.showwarning(
                    'Atenção!',
                    'Nome e e-mail são obrigatórios!',
                    parent=janela
                )
                return

            if not email_valido(email):
                messagebox.showwarning(
                    'Atenção!',
                    'Digite um e-mail válido!',
                    parent=janela
                )
                return

            if senha and len(senha) < SENHA_MINIMA:
                messagebox.showwarning(
                    'Atenção!',
                    f'A senha deve possuir pelo menos {SENHA_MINIMA} caracteres.',
                    parent=janela
                )
                return

            usuario_editado = Usuario(nome, email, senha)

            # O id identifica o registro a ser atualizado na base de dados
            sucesso, mensagem = usuario_editado.atualizar(usuario['id'])

            if sucesso:
                messagebox.showinfo('Sucesso', mensagem, parent=janela)
                janela.destroy()
                self.listar_usuarios()
            else:
                messagebox.showerror('Erro', mensagem, parent=janela)

        ttk.Button(
            frame,
            text='Salvar alteração',
            command=salvar_alteracao
        ).pack()


# Função de inicialização da aplicação
def executar():
    root = tk.Tk()

    # Garante que o banco e a tabela existem antes de montar a janela
    sucesso, mensagem = criar_banco()
    if not sucesso:
        messagebox.showerror(
            'Erro de conexão',
            mensagem + '\n\nConfira as credenciais no arquivo .env.'
        )
        root.destroy()
        return

    Aplicacao(root)

    # Mantém a janela aberta ouvindo os eventos (cliques, teclado, etc.)
    root.mainloop()