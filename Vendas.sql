/****** Object:  Table [dbo].[tb_venda]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_venda](
	[id_venda] [numeric](18, 0) IDENTITY(1,1) NOT NULL,
	[data_venda] [datetime] NOT NULL,
	[id_cliente] [int] NOT NULL,
 CONSTRAINT [PK_tb_venda] PRIMARY KEY CLUSTERED 
(
	[id_venda] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tb_departamento]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_departamento](
	[id_departamento] [int] IDENTITY(1,1) NOT NULL,
	[nome_departamento] [varchar](50) NOT NULL,
 CONSTRAINT [PK_tb_departamento] PRIMARY KEY CLUSTERED 
(
	[id_departamento] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tb_produto]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_produto](
	[id_produto] [int] IDENTITY(1,1) NOT NULL,
	[descricao] [varchar](50) NOT NULL,
	[preco_sugerido] [numeric](18, 2) NOT NULL,
	[id_departamento] [int] NOT NULL,
 CONSTRAINT [PK_tb_produto] PRIMARY KEY CLUSTERED 
(
	[id_produto] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[tb_cliente]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_cliente](
	[id_cliente] [int] IDENTITY(1,1) NOT NULL,
	[nome_cliente] [varchar](50) NOT NULL,
	[tipo_cliente] [varchar](1) NOT NULL,
 CONSTRAINT [PK_tb_cliente] PRIMARY KEY CLUSTERED 
(
	[id_cliente] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  View [dbo].[vw_Consulta_Venda]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[vw_Consulta_Venda]
AS
SELECT        dbo.tb_produto_venda.id_detalhe_venda, dbo.tb_produto_venda.id_venda, dbo.tb_venda.data_venda, dbo.tb_venda.id_cliente, dbo.tb_cliente.nome_cliente, dbo.tb_cliente.tipo_cliente, dbo.tb_produto_venda.id_produto, 
                         dbo.tb_produto.descricao, dbo.tb_produto.preco_sugerido, dbo.tb_produto.id_departamento, dbo.tb_departamento.nome_departamento
FROM            dbo.tb_produto INNER JOIN
                         dbo.tb_departamento ON dbo.tb_produto.id_departamento = dbo.tb_departamento.id_departamento INNER JOIN
                         dbo.tb_produto_venda ON dbo.tb_produto.id_produto = dbo.tb_produto_venda.id_produto INNER JOIN
                         dbo.tb_venda ON dbo.tb_produto_venda.id_venda = dbo.tb_venda.id_venda INNER JOIN
                         dbo.tb_cliente ON dbo.tb_venda.id_cliente = dbo.tb_cliente.id_cliente
GO
/****** Object:  Table [dbo].[tb_detalhe_venda]    Script Date: 4/17/2024 9:08:22 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tb_detalhe_venda](
	[id_detalhe_venda] [numeric](18, 0) IDENTITY(1,1) NOT NULL,
	[id_venda] [numeric](18, 0) NOT NULL,
	[id_produto] [int] NOT NULL,
	[quantidade_produto] [numeric](18, 2) NOT NULL,
	[preco_unitario_venda] [numeric](18, 2) NOT NULL,
 CONSTRAINT [PK_tb_detalhe_venda] PRIMARY KEY CLUSTERED 
(
	[id_detalhe_venda] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[tb_detalhe_venda]  WITH CHECK ADD  CONSTRAINT [FK_tb_detalhe_venda_tb_produto] FOREIGN KEY([id_produto])
REFERENCES [dbo].[tb_produto] ([id_produto])
GO
ALTER TABLE [dbo].[tb_detalhe_venda] CHECK CONSTRAINT [FK_tb_detalhe_venda_tb_produto]
GO
ALTER TABLE [dbo].[tb_detalhe_venda]  WITH CHECK ADD  CONSTRAINT [FK_tb_detalhe_venda_tb_venda] FOREIGN KEY([id_venda])
REFERENCES [dbo].[tb_venda] ([id_venda])
GO
ALTER TABLE [dbo].[tb_detalhe_venda] CHECK CONSTRAINT [FK_tb_detalhe_venda_tb_venda]
GO
ALTER TABLE [dbo].[tb_produto]  WITH CHECK ADD  CONSTRAINT [FK_tb_produto_tb_departamento] FOREIGN KEY([id_departamento])
REFERENCES [dbo].[tb_departamento] ([id_departamento])
GO
ALTER TABLE [dbo].[tb_produto] CHECK CONSTRAINT [FK_tb_produto_tb_departamento]
GO
ALTER TABLE [dbo].[tb_venda]  WITH CHECK ADD  CONSTRAINT [FK_tb_venda_tb_cliente] FOREIGN KEY([id_cliente])
REFERENCES [dbo].[tb_cliente] ([id_cliente])
GO
ALTER TABLE [dbo].[tb_venda] CHECK CONSTRAINT [FK_tb_venda_tb_cliente]
GO
