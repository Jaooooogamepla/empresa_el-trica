import sqlite3
from datetime import datetime

class SistemaElectrico:
    def __init__(self):
        self.criar_banco()
    
    def criar_banco(self):
        """Cria o banco de dados e tabelas"""
        self.conn = sqlite3.connect(':memory:')  
        self.cursor = self.conn.cursor()
     
        self.cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                cargo TEXT DEFAULT 'funcionario'
            )
        ''')
  
        self.cursor.execute('''
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj_cpf TEXT,
                telefone TEXT,
                email TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                cliente_id INTEGER,
                status TEXT DEFAULT 'Ativo',
                data_inicio DATE,
                data_termino DATE,
                orcamento REAL DEFAULT 0.0
            )
        ''')

        self.inserir_dados_iniciais()
        self.conn.commit()
    
    def inserir_dados_iniciais(self):
        """Insere dados de exemplo"""

        usuarios = [
            ('Administrador', 'admin@email.com', '123456', 'gerente'),
            ('Maria Silva', 'maria@email.com', '123456', 'eletricista'),
            ('João Santos', 'joao@email.com', '123456', 'engenheiro')
        ]
        
        self.cursor.executemany(
            "INSERT INTO usuarios (nome, email, senha, cargo) VALUES (?, ?, ?, ?)",
            usuarios
        )
        
        clientes = [
            ('João Silva Construtora', '12.345.678/0001-90', '(11) 9999-8888', 'joao@construtora.com'),
            ('Empresa ABC Ltda', '98.765.432/0001-10', '(11) 7777-6666', 'contato@empresaabc.com'),
            ('Maria Oliveira', '123.456.789-00', '(11) 8888-9999', 'maria@email.com'),
            ('Shopping Center Plaza', '23.456.789/0001-11', '(11) 3333-4444', 'shopping@plaza.com')
        ]
        
        self.cursor.executemany(
            "INSERT INTO clientes (nome, cnpj_cpf, telefone, email) VALUES (?, ?, ?, ?)",
            clientes
        )

        projetos = [
            ('Instalação Elétrica Predial', 'Instalação completa do prédio comercial', 1, 'Em Andamento', '2024-01-01', '2024-03-01', 25000.00),
            ('Subestação de Energia', 'Construção de subestação 138kV', 2, 'Planejamento', '2024-02-01', '2024-06-01', 150000.00),
            ('Manutenção Preventiva', 'Manutenção do sistema elétrico', 3, 'Concluído', '2024-01-15', '2024-01-20', 5000.00),
            ('Iluminação Shopping', 'Projeto completo de iluminação', 4, 'Em Andamento', '2024-01-10', '2024-04-10', 80000.00)
        ]
        
        self.cursor.executemany(
            "INSERT INTO projetos (nome, descricao, cliente_id, status, data_inicio, data_termino, orcamento) VALUES (?, ?, ?, ?, ?, ?, ?)",
            projetos
        )
    
    def login(self, email, senha):
        """Faz login no sistema"""
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )
        return self.cursor.fetchone()
    
    def listar_clientes(self):
        """Lista todos os clientes"""
        self.cursor.execute("SELECT * FROM clientes ORDER BY nome")
        return self.cursor.fetchall()
    
    def cadastrar_cliente(self, nome, cnpj_cpf, telefone, email):
        """Cadastra novo cliente"""
        try:
            self.cursor.execute(
                "INSERT INTO clientes (nome, cnpj_cpf, telefone, email) VALUES (?, ?, ?, ?)",
                (nome, cnpj_cpf, telefone, email)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
    
    def listar_projetos(self):
        """Lista todos os projetos com nome do cliente"""
        self.cursor.execute('''
            SELECT p.*, c.nome as cliente_nome 
            FROM projetos p 
            LEFT JOIN clientes c ON p.cliente_id = c.id 
            ORDER BY p.status
        ''')
        return self.cursor.fetchall()
    
    def cadastrar_projeto(self, nome, descricao, cliente_id, data_inicio, data_termino, orcamento):
        """Cadastra novo projeto"""
        try:
            self.cursor.execute(
                "INSERT INTO projetos (nome, descricao, cliente_id, data_inicio, data_termino, orcamento) VALUES (?, ?, ?, ?, ?, ?)",
                (nome, descricao, cliente_id, data_inicio, data_termino, orcamento)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro: {e}")
            return False
    
    def get_estatisticas(self):
        """Retorna estatísticas do sistema"""
        self.cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM projetos")
        total_projetos = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM projetos WHERE status = 'Em Andamento'")
        projetos_ativos = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT SUM(orcamento) FROM projetos WHERE status = 'Em Andamento'")
        faturamento = self.cursor.fetchone()[0] or 0
        
        return total_clientes, total_projetos, projetos_ativos, faturamento

def mostrar_menu_principal(usuario):
    """Mostra o menu principal"""
    print("\n" + "="*60)
    print(f"🏗️  SISTEMA JANOL.INEJ - EMPRESA ELÉTRICA")
    print(f"👤 Usuário: {usuario[1]} ({usuario[4]})")
    print("="*60)
    print("1. 📊 Dashboard")
    print("2. 👥 Clientes")
    print("3. 🏗️ Projetos")
    print("4. 📋 Relatórios")
    print("5. 🚪 Sair")
    print("="*60)

def mostrar_dashboard(sistema):
    """Mostra o dashboard do sistema"""
    clientes, projetos, ativos, faturamento = sistema.get_estatisticas()
    
    print("\n📊 DASHBOARD - RESUMO DO SISTEMA")
    print("-" * 50)
    print(f"👥 Total de Clientes: {clientes}")
    print(f"🏗️ Total de Projetos: {projetos}")
    print(f"⚡ Projetos Ativos: {ativos}")
    print(f"💰 Faturamento em Andamento: R$ {faturamento:,.2f}")
    print("-" * 50)

    projetos = sistema.listar_projetos()[:3]
    print("\n📋 ÚLTIMOS PROJETOS:")
    for projeto in projetos:
        status_emoji = "🟢" if projeto[4] == 'Em Andamento' else "🟡" if projeto[4] == 'Planejamento' else "🔵"
        print(f"  {status_emoji} {projeto[1]} - {projeto[8]} (R$ {projeto[7]:,.2f})")

def gerenciar_clientes(sistema):
    """Gerencia os clientes"""
    while True:
        print("\n👥 GERENCIAMENTO DE CLIENTES")
        print("1. 📋 Listar Clientes")
        print("2. ➕ Cadastrar Novo Cliente")
        print("3. ↩️ Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            clientes = sistema.listar_clientes()
            print("\n📋 LISTA DE CLIENTES:")
            print("-" * 90)
            print(f"{'ID':<3} {'NOME':<25} {'CNPJ/CPF':<20} {'TELEFONE':<15} {'EMAIL'}")
            print("-" * 90)
            for cliente in clientes:
                print(f"{cliente[0]:<3} {cliente[1]:<25} {cliente[2]:<20} {cliente[3]:<15} {cliente[4]}")
            print("-" * 90)
            
        elif opcao == '2':
            print("\n➕ CADASTRAR NOVO CLIENTE")
            print("-" * 40)
            nome = input("Nome/Razão Social: ")
            cnpj_cpf = input("CNPJ/CPF: ")
            telefone = input("Telefone: ")
            email = input("Email: ")
            
            if sistema.cadastrar_cliente(nome, cnpj_cpf, telefone, email):
                print("✅ Cliente cadastrado com sucesso!")
            else:
                print("❌ Erro ao cadastrar cliente!")
                
        elif opcao == '3':
            break
        else:
            print("❌ Opção inválida!")

def gerenciar_projetos(sistema):
    """Gerencia os projetos"""
    while True:
        print("\n🏗️ GERENCIAMENTO DE PROJETOS")
        print("1. 📋 Listar Projetos")
        print("2. ➕ Cadastrar Novo Projeto")
        print("3. ↩️ Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            projetos = sistema.listar_projetos()
            print("\n📋 LISTA DE PROJETOS:")
            print("-" * 120)
            print(f"{'NOME':<25} {'CLIENTE':<20} {'STATUS':<15} {'ORÇAMENTO':<12} {'INÍCIO':<12} {'TÉRMINO':<12}")
            print("-" * 120)
            for projeto in projetos:
                status_emoji = "🟢" if projeto[4] == 'Em Andamento' else "🟡" if projeto[4] == 'Planejamento' else "🔵"
                print(f"{status_emoji} {projeto[1]:<23} {projeto[8]:<19} {projeto[4]:<14} R$ {projeto[7]:<8,.0f} {projeto[5]:<11} {projeto[6]:<11}")
            print("-" * 120)
            
        elif opcao == '2':
            print("\n➕ CADASTRAR NOVO PROJETO")
            print("-" * 40)
            nome = input("Nome do Projeto: ")
            descricao = input("Descrição: ")
            
            # Listar clientes para escolha
            clientes = sistema.listar_clientes()
            print("\n👥 CLIENTES DISPONÍVEIS:")
            for cliente in clientes:
                print(f"ID: {cliente[0]} - {cliente[1]}")
            
            try:
                cliente_id = int(input("\nID do Cliente: "))
                data_inicio = input("Data Início (YYYY-MM-DD): ")
                data_termino = input("Data Término (YYYY-MM-DD): ")
                orcamento = float(input("Orçamento (R$): "))
                
                if sistema.cadastrar_projeto(nome, descricao, cliente_id, data_inicio, data_termino, orcamento):
                    print("✅ Projeto cadastrado com sucesso!")
                else:
                    print("❌ Erro ao cadastrar projeto!")
            except ValueError:
                print("❌ Erro: ID deve ser número e orçamento deve ser valor!")
                
        elif opcao == '3':
            break
        else:
            print("❌ Opção inválida!")

def mostrar_relatorios(sistema):
    """Mostra relatórios do sistema"""
    print("\n📋 RELATÓRIOS DO SISTEMA")
    print("=" * 50)
    
    clientes, projetos, ativos, faturamento = sistema.get_estatisticas()
    
    print(f"📈 ESTATÍSTICAS GERAIS:")
    print(f"   • Total de Clientes: {clientes}")
    print(f"   • Total de Projetos: {projetos}")
    print(f"   • Projetos Ativos: {ativos}")
    print(f"   • Taxa de Conclusão: {(projetos - ativos) / projetos * 100:.1f}%" if projetos > 0 else "   • Taxa de Conclusão: 0%")
    
    print(f"\n💰 INFORMAÇÕES FINANCEIRAS:")
    print(f"   • Faturamento em Andamento: R$ {faturamento:,.2f}")
    print(f"   • Custo Médio por Projeto: R$ {faturamento/projetos:,.2f}" if projetos > 0 else "   • Custo Médio por Projeto: R$ 0,00")
    print(f"   • Lucro Estimado (30%): R$ {faturamento * 0.3:,.2f}")

def main():
    sistema = SistemaElectrico()
    
    print("🏗️  BEM-VINDO AO SISTEMA JANOL.INEJ")
    print("=" * 60)
    print("💡 Dica: Use admin@email.com / 123456 para login")
    print("=" * 60)

    while True:
        print("\n🔐 FAÇA SEU LOGIN")
        email = input("Email: ")
        senha = input("Senha: ")
        
        usuario = sistema.login(email, senha)
        if usuario:
            print(f"\n✅ Login realizado com sucesso! Bem-vindo, {usuario[1]}!")
            break
        else:
            print("❌ Email ou senha incorretos!")
            print("💡 Tente: admin@email.com / 123456")
   
    while True:
        mostrar_menu_principal(usuario)
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            mostrar_dashboard(sistema)
        elif opcao == '2':
            gerenciar_clientes(sistema)
        elif opcao == '3':
            gerenciar_projetos(sistema)
        elif opcao == '4':
            mostrar_relatorios(sistema)
        elif opcao == '5':
            print("\n👋 Obrigado por usar o Sistema Janol.Inej!")
            print("💡 Empresa Elétrica - Serviços de Qualidade")
            break
        else:
            print("❌ Opção inválida!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
