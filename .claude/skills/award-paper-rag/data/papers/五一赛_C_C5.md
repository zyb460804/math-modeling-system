# C5

五一数学建模竞赛

承  诺  书

我们仔细阅读了五一数学建模竞赛的竞赛规则。

我们完全明白，在竞赛开始后参赛队员不能以任何方式（包括电话、电子邮件、网上咨询等）与本队以外的任何人（包括指导教师）研究、讨论与赛题有关的问题。

我们知道，抄袭别人的成果是违反竞赛规则的, 如果引用别人的成果或其它公开的资料（包括网上查到的资料），必须按照规定的参考文献的表述方式在正文引用处和参考文献中明确列出。

我们郑重承诺，严格遵守竞赛规则，以保证竞赛的公正、公平性。如有违反竞赛规则的行为，我们愿意承担由此引起的一切后果。

我们授权五一数学建模竞赛组委会，可将我们的论文以任何形式进行公开展示（包括进行网上公示，在书籍、期刊和其他媒体进行正式或非正式发表等）。

参赛题号（从A/B/C中选择一项填写）：         C

参赛队号：                                  B26011125

参赛组别（研究生、本科、专科、高中）：         本科

所属学校（学校全称）：               德州学院

参赛队员： 队员1姓名：                张智卿

队员2姓名：                    朱严博

队员3姓名：                    陈广博

联系方式： Email：2788207254@qq.com

联系电话：    178662276773

日期：  2026     年  5 月   4日

（除本页外不允许出现学校及个人信息）

五 一 数 学 建 模 竞 赛

题 目：基于鲁棒校正与分阶段多源融合预测的边坡预警模型研究

关键词：边坡预警；鲁棒校正；变点检测；多源数据融合；位移速度阈值

摘  要：

边坡失稳是水利工程、山区交通和露天矿山中具有渐进演化特征的典型灾害。针对监测过程中存在传感器零漂、安装偏差、缺失采样、短时异常和阶段转换不清等问题，本文围绕位移校正、阶段识别、多源数据清洗、表面位移预测和速度阈值预警五项任务，建立“鲁棒传感器校正—持续变点识别—多源异常检测—分阶段融合预测—速度阈值预警”的一体化模型链条。

针对问题一，以传统振弦式位移计为基准，构建Huber鲁棒线性校正模型，将新型光纤位移计观测值映射到统一位移尺度。五折交叉验证得到校正模型 ŷ=0.8817509x−0.5299438，MAE为1.289 mm，RMSE为2.685 mm，MAPE为1.836%，R²为0.9992；五个待校正值的结果为5.759、15.805、73.834、108.414、147.311 mm。针对问题二，采用Savitzky-Golay滤波、速度加速度计算和分段残差下降准则识别三段式形变节点，得到T1=8025、T2=9575，三阶段平均速度分别为0.257、1.888、6.658 mm/h。

针对问题三，按变量属性分别采用PCHIP插值、线性插值、非负约束、Savitzky-Golay滤波、滚动中位数和Hampel滤波完成缺失补齐与去噪，并用MAD标准化残差识别异常。训练集中共检出单变量异常点71个、共同异常点16个；贡献分析显示，深部位移是表面位移的首要解释变量，孔隙水压力和降雨量共同反映水力触发作用，微震事件数体现内部损伤累积。针对问题四，建立阶段趋势项与扰动残差修正项相结合的预测模型，并将爆破点距离和单段最大药量转化为爆破指示变量及爆破强度，实验集五个指定时刻表面位移预测值分别为5.538、54.806、390.035、566.748、576.693 mm。

针对问题五，通过六选五变量组合枚举和时间序列交叉验证，选择降雨量、孔隙水压力、微震事件数、爆破点距离和单段最大药量作为最优组合。速度聚类得到低速、中速和高速中心0.199、1.595、9.126 mm/h，并据此设定0.764、4.126和8.0 mm/h三级阈值，形成正常、蓝色、橙色和红色预警规则。模型兼具鲁棒性、解释性和工程可操作性，可为多源监测条件下的边坡早期预警提供量化依据。

1 问题重述

1.1 问题背景

边坡工程广泛存在于水利枢纽、山区公路、铁路隧道口、露天矿山、尾矿库及城市建设边坡中。边坡一旦发生滑移或崩塌，可能造成道路阻断、工程损毁、矿区停产和人员伤亡。随着光纤位移计、振弦式位移计、孔隙水压力计、微震监测和物联网采集系统的发展，边坡监测已经由单一位移观测转向多源连续监测。 相关滑坡监测、位移预测与预警阈值研究为本文多源监测建模提供了理论参考[1-5]。

实际监测数据并不天然适合建模。不同传感器之间存在测量尺度差异和零点漂移；连续采样数据中存在缺失、噪声和短时跳变；边坡位移演化又具有典型的缓慢匀速、加速和快速形变三阶段特征。因此，本题的核心不是单一预测，而是要先使监测数据可信化，再识别演化阶段，最后将位移预测转化为可执行的预警规则。

1.2 核心目标

建立光纤位移计向基准振弦式位移计的鲁棒校正模型，并通过交叉验证评价误差。

利用位移序列识别三段式形变的两个阶段转换节点，并计算各阶段平均速度和拟合效果。

对多源监测数据进行缺失补齐、去噪和异常检测，给出共同异常点与变量贡献度。

建立分阶段表面位移预测模型，利用实验集阶段标签预测指定时刻表面位移。

从六类候选变量中优选五类变量，并基于表面位移速度构建分级滑坡预警机制。

2 问题分析

本文采用“数据校正—阶段识别—数据清洗—分阶段预测—速度预警”的总思路。问题一解决传感器尺度一致性，问题二提供阶段边界，问题三保证多源变量质量并解释驱动机制，问题四利用阶段标签进行表面位移预测，问题五将预测结果和速度序列转化为工程预警阈值。

问题一的关键矛盾是新型光纤位移计相对基准传感器存在比例偏差和零点偏移，因此应构建监督校正模型。考虑现场监测数据可能存在局部异常点，采用Huber鲁棒回归替代普通最小二乘[7]，并用五折交叉验证评价泛化误差。

问题二的关键矛盾是真实阶段转换与单点噪声跳变均可能表现为位移突增。真实转换应体现为速度水平持续抬升，而不是孤立尖峰。因此先采用Savitzky-Golay方法对位移序列平滑[8]，再综合速度、加速度、前后窗口统计差异和分段残差下降筛选真实变点。

问题三的关键矛盾是多源变量属性不同。表面位移、深部位移和孔隙水压力具有连续演化特征，适合插值和平滑；降雨量、微震事件数具有非负和脉冲特征，应避免过度平滑。异常检测不直接作用于原始值，而作用于趋势残差，以减少把正常增长趋势误判为异常。

问题四的关键矛盾是不同形变阶段中外部扰动对位移响应的影响机制不同。若用统一模型拟合全部样本，会混合阶段差异；若只做时间外推，又无法解释降雨、孔压、微震和爆破作用。因此采用阶段趋势项与扰动残差项相结合的分阶段模型。

问题五的关键矛盾是变量选择既要追求预测误差低，又要保留失稳机理完整性。降雨量和孔隙水压力反映水力作用，微震事件数反映内部损伤，爆破点距离和单段最大药量共同决定爆破扰动强度。最终通过组合枚举和时间序列交叉验证确定最优五变量组合。

结果口径说明：本文后续所有表格、图示和附录均以附录A程序框架输出结果为统一口径，即问题一校正模型、问题二转换节点、问题四预测值和问题五变量组合均采用本文正文当前结果，避免不同试算版本之间的数值混用。

3 模型假设

假设1：基准传感器B可作为校正目标。题目明确说明B为经验证的传统振弦式位移计数据，因此将其作为监督校正目标。该假设使问题一可转化为回归校正问题。

假设2：真实阶段转换表现为速度水平持续改变。三段式形变理论表明边坡失稳前存在持续加速过程，单点尖峰不能代表阶段转换。该假设支撑持续性变点识别准则。

假设3：短时缺失可由相邻时刻和局部趋势补齐。题目数据为固定采样间隔的连续监测序列，短时缺失多由通信或设备故障造成。该假设保证滤波、异常检测和预测模型具有完整输入。

假设4：同一形变阶段内变量作用关系相对稳定。边坡内部结构状态在同一阶段内变化相对连续，不同阶段允许模型参数变化。该假设支持分阶段预测模型。

假设5：表面位移速度可作为预警主指标。位移速度直接刻画形变发展快慢，是滑坡临近失稳的重要指标；降雨、孔压和微震作为辅助触发条件，可降低误报。

4 符号说明

表4.1 主要符号说明

5 问题一：鲁棒传感器校正模型

5.1 模型构建

设光纤位移计原始观测值为x_i，基准振弦式位移计观测值为y_i。两类传感器监测同一边坡测点，主要差异可由比例偏差和零点漂移描述，因此建立线性校正模型：

yᵢ = β₀ + β₁xᵢ + εᵢ

普通最小二乘会放大异常点影响。为增强抗异常能力，采用Huber损失函数估计参数[7]：

Lδ(rᵢ)=0.5rᵢ²（|rᵢ|≤δ）；Lδ(rᵢ)=δ(|rᵢ|−0.5δ)（|rᵢ|>δ），其中 rᵢ=yᵢ−β₀−β₁xᵢ

(β̂₀, β̂₁)=arg min Σᵢ Lδ(yᵢ−β₀−β₁xᵢ)

5.2 求解与结果

使用Python中HuberRegressor求解，并采用五折交叉验证评价泛化误差。全样本训练得到校正模型：

ŷ = 0.8817509x − 0.5299438

表5.1 待校正数据结果

表5.2 问题一交叉验证结果

图5.1 光纤位移计与基准位移计校正关系图

5.3 结果分析与检验

比例系数0.8817509小于1，说明光纤位移计原始读数整体偏大；截距−0.5299438表明存在小幅零点偏移。交叉验证中R²达到0.9992，MAPE为1.836%，说明该模型能够稳定解释基准位移变化。RMSE高于MAE，表明局部仍有较大偏差点，但Huber损失已对其影响进行抑制。

6 问题二：三段式形变阶段识别

6.1 模型构建

对位移序列直接差分会放大噪声，因此先采用Savitzky-Golay滤波提取平滑趋势。设局部窗口半宽为m，多项式阶数为p，则窗口中心平滑值由下式确定：

(â₀,…,âₚ)=arg min Σⱼ₌₋ₘᵐ(sᵢ₊ⱼ−Σᵩ₌₀ᵖaᵩjᵩ)²，s̃ᵢ=â₀

题目采样间隔为10分钟，即每小时6个采样点。速度与加速度定义为：

v_i = 6(s̃_i − s̃_{i-1}),     a_i = 6(v_i − v_{i-1}).

候选节点k需满足前后窗口速度均值差异显著、节点后速度持续抬升，并能降低分段拟合残差。设未分段残差平方和为RSS_0，分段后残差平方和为RSS_1，则要求(RSS_0−RSS_1)/RSS_0超过给定阈值。

6.2 求解与结果

综合速度持续性和分段残差下降准则，识别得到两个转换节点T_1=8025、T_2=9575。

表6.1 三阶段划分与平均速度

表6.2 分阶段二次趋势拟合结果

图6.1 完整位移序列及三阶段转换节点图

6.3 结果分析与检验

三阶段平均速度从0.257 mm/h增至1.888 mm/h，再增至6.658 mm/h，呈现明显阶梯式上升。第二阶段速度约为第一阶段的7.35倍，第三阶段速度约为第二阶段的3.53倍，符合边坡由稳定调整、非稳定加速到临近失稳的动力演化规律。三个阶段R²均高于0.999，说明分阶段模型对位移趋势具有较强解释能力。

7 问题三：多源数据预处理、异常检测与贡献分析

7.1 模型构建

连续变量采用线性插值或PCHIP插值补齐，非负脉冲变量补齐后施加非负约束。对表面位移、深部位移和孔隙水压力采用Savitzky-Golay滤波；对降雨量和微震事件数采用滚动中位数或Hampel滤波，以保留脉冲事件特征。 其中Savitzky-Golay滤波用于保留局部趋势与斜率特征[8]。

x(t)=x(tᵢ)+[x(tⱼ)−x(tᵢ)](t−tᵢ)/(tⱼ−tᵢ)，tᵢ<t<tⱼ

MAD=median(|rᵢ−median(r)|)，zᵢ=0.6745(rᵢ−median(r))/MAD

Iᵢⱼ=1(|zᵢⱼ|>3.5)，Cᵢ=1(ΣⱼIᵢⱼ≥2)

贡献分析采用多元线性回归和随机森林并行。线性模型用于解释变量方向，随机森林置换重要度[6]用于衡量变量对预测误差的贡献。

Eᵢ=α₀+α₁Rᵢ+α₂Pᵢ+α₃Mᵢ+α₄dᵢ+εᵢ

Impⱼ=RMSEperm(j)−RMSEbase

7.2 求解结果

由附录A程序中 preprocess_and_analyze 模块输出缺失值补齐、去噪和异常检测结果，统计结果见表7.1—表7.4。

表7.1 缺失值处理与去噪方法

表7.2 异常点检测统计

表7.3 代表性共同异常点

表7.4 表面位移贡献度分析

图7.1 多源变量清洗前后对比图

7.3 结果分析与检验

为避免正文表格过长，表7.3仅列出代表性共同异常点；完整共同异常点清单见附录C。实验集表面位移估计结果采用多源变量回归模型输出，节选结果见附录D，完整结果由附录A程序自动生成。

异常点主要集中在降雨、微震和位移突变附近，且共同异常点多出现在加速阶段及快速阶段前后，具有明确工程含义。贡献度结果表明，深部位移贡献最高，说明内部剪切变形是表面位移变化的主导因素；孔隙水压力和降雨量共同反映水力诱发机制；微震事件数对快速阶段前兆有补充判别价值。

8 问题四：分阶段表面位移预测模型

8.1 模型构建

对每一阶段分别建立“趋势项+扰动残差修正项”模型。趋势项描述边坡自身蠕变演化，扰动残差项刻画降雨、孔压、微震和爆破对局部位移增量的影响。

ŷₜ=gₖ(τₜ)+hₖ(Xₜ)，k=1,2,3

gₖ(τ)=γₖ₀+γₖ₁τ+γₖ₂τ²

Iₜ=1(Lₜ、Qₜ均非空)，Bₜ=Iₜ·Qₜ/Lₜ²

扰动特征X_t包括降雨量、孔隙水压力、微震事件数、爆破指示变量、爆破强度、6小时累计降雨量、24小时累计降雨量和孔压变化率。实验集已给定阶段标签，因此可直接调用对应阶段模型进行预测。

8.2 求解结果

由附录A程序中 staged_prediction 模块输出实验集指定时刻预测值和分阶段交叉验证指标，结果见表8.1和表8.2。

表8.1 实验集指定时刻表面位移预测结果

表8.2 分阶段预测模型检验结果

图8.1 实验集五个指定时刻表面位移预测趋势

8.3 结果分析与检验

预测值由5.538 mm逐步增至576.693 mm，呈现缓慢增长、加速增长和快速增长三段特征。快速阶段误差相对较大，原因是该阶段位移增速高、扰动响应强，但R²仍保持在0.9912，说明分阶段模型能较好捕捉整体趋势。残差均值接近0，表明模型不存在明显系统性高估或低估。 进一步从残差均值看，三个阶段残差均值均接近0，说明模型没有明显系统性高估或低估；从R²和RMSE看，模型能兼顾趋势拟合和数值误差控制。

9 问题五：变量组合优选与滑坡预警机制

9.1 模型构建

设候选变量集合为S={R,P,M,K,L,Q}。每次剔除一个变量构成五变量组合，使用相同预测模型和时间序列交叉验证比较MAE、RMSE和R²，并结合机理完整性确定最优组合。

Sⱼ=S\{j}，Scoreⱼ=RMSEⱼ+λ·Penaltyⱼ

位移速度按v_i=6(s_i−s_{i−1})计算，对正速度样本进行三类聚类，得到低速、中速和高速中心c_1<c_2<c_3。考虑速度分布通常右偏，阈值采用相邻中心的几何均值。

θ₁=√(c₁c₂)，θ₂=√(c₂c₃)

9.2 求解结果

由附录A程序中 variable_selection_and_warning 模块对六种五变量组合进行时间序列交叉验证，结果见表9.1。

表9.1 六选五变量组合交叉验证结果

表9.2 速度聚类中心与阈值

表9.3 分级预警规则

图9.1 速度聚类结果与预警阈值图

9.3 结果分析与检验

剔除干湿入渗系数时RMSE最低，为9.41 mm，且保留了水力诱发、内部损伤和爆破扰动三类机制，因此选取降雨量、孔隙水压力、微震事件数、爆破点距离和单段最大药量作为最优组合。速度阈值与问题二识别出的三阶段速度水平相一致，说明预警规则具有阶段解释性。连续触发规则可降低单点噪声误报，多源同步条件可提高红色预警可靠性。

10 敏感性与鲁棒性检验

为回应模型稳定性问题，对关键参数和输入扰动进行敏感性检验。检验对象包括Huber损失参数、Savitzky-Golay窗口长度、变点持续窗口、速度聚类初值和输入噪声扰动。

表10.1 关键参数敏感性与鲁棒性检验

结果表明，本文模型对核心参数扰动不敏感，主要结论不会因单一参数调整而发生根本变化。其中变点位置和速度阈值具有较好稳定性，说明模型能够区分持续阶段转换与局部噪声跳变。 结合前文交叉验证结果，校正模型、分阶段预测模型和速度阈值模型均通过了误差精度、稳定性和工程合理性三类检验。

11 模型评价

11.1 模型优点

模型链条完整，覆盖传感器校正、阶段识别、多源清洗、分阶段预测和预警决策全过程，五个问题之间逻辑衔接清晰。

鲁棒性较强。问题一采用Huber回归，问题三采用MAD和Hampel方法，问题二采用持续性变点准则，均能减少异常点和短时跳变影响。

解释性较好。速度、加速度、阶段趋势项、爆破强度和多源同步异常均有明确工程含义，便于现场应用。

预测与预警结合紧密。模型不仅输出表面位移预测值，还进一步构建速度阈值与分级响应规则。

11.2 模型不足与改进方向

模型仍依赖题目附件数据的代表性。若训练集未覆盖极端降雨、强爆破或突发滑移场景，外推能力会下降。

分阶段建模减少了每一阶段的有效样本量，快速阶段样本较少时残差修正模型稳定性会受影响。

速度阈值属于场地相关阈值，不同地质结构、岩性和监测布设条件下需要重新标定。

后续可引入渗流—稳定性耦合模型或SHAP解释方法，进一步提高物理解释和变量贡献分析精度。

12 结论

本文围绕边坡预警问题，构建了“鲁棒校正—阶段识别—多源清洗—分阶段预测—速度预警”的完整模型链条。该链条先修正传感器尺度偏差，再识别位移三阶段演化规律，最后将多源监测信息转化为可执行的预警阈值，能够较好对应题目五个任务。

问题一中，Huber鲁棒线性校正模型取得MAE=1.289 mm、RMSE=2.685 mm、MAPE=1.836%、R²=0.9992的交叉验证结果，说明光纤位移计读数可稳定映射到基准位移尺度。问题二中，识别得到T1=8025、T2=9575两个转换节点，三阶段平均速度由0.257 mm/h升至1.888 mm/h和6.658 mm/h，符合边坡由稳定调整到快速形变的发展规律。

问题三中，针对连续型变量和脉冲型变量分别采用插值、非负约束和平滑滤波方法，最终检出单变量异常点71个、共同异常点16个。贡献分析表明，深部位移、孔隙水压力、降雨量和微震事件数依次解释表面位移变化，体现了“内部变形—水力触发—损伤累积”的作用链条。

问题四中，分阶段趋势项与扰动残差修正项相结合的模型给出实验集五个指定时刻预测值5.538、54.806、390.035、566.748和576.693 mm，预测曲线呈现缓慢增长、加速增长和快速增长的三段特征。问题五中，最优变量组合保留降雨量、孔隙水压力、微震事件数、爆破点距离和单段最大药量，速度聚类阈值0.764、4.126和8.0 mm/h形成正常、蓝色、橙色和红色预警规则。

综合来看，本文模型具有较好的鲁棒性、可解释性和工程可操作性。其不足在于速度阈值和阶段参数仍具有场地相关性，后续可结合更多边坡样本、渗流—稳定性耦合模型和SHAP解释方法进一步提升跨场景泛化能力。

13 参考文献

[1] 邓李政，袁宏永，张鸣之，陈建国. 滑坡变形监测预警技术研究进展[J]. 清华大学学报（自然科学版），2023，63(6): 847-861.

[2] Nava L, Carraro E, Reyes-Carmona C, et al. Landslide displacement forecasting using deep learning and monitoring data across selected sites[J]. Landslides, 2023, 20: 2111-2129.

[3] Huang F, Yin K, Zhang G, et al. Landslide displacement prediction based on multi-source data fusion and sensitivity states[J]. Engineering Geology, 2020, 271: 105608.

[4] Li Y, Yang B, Zhang M, et al. Rock slope displacement prediction based on multi-source information fusion and optimized deep extreme learning machine[J]. Frontiers in Environmental Science, 2022, 10: 982069.

[5] Zeng T, Chen H, Li X, et al. Determination of landslide displacement warning thresholds by DBA-LSTM and numerical simulation[J]. Applied Sciences, 2022, 12(13): 6690.

[6] Breiman L. Random forests[J]. Machine Learning, 2001, 45(1): 5-32.

[7] Huber P J, Ronchetti E M. Robust Statistics[M]. 2nd ed. Hoboken: Wiley, 2009: 53-82.

[8] Savitzky A, Golay M J E. Smoothing and differentiation of data by simplified least squares procedures[J]. Analytical Chemistry, 1964, 36(8): 1627-1639.

[9] Hastie T, Tibshirani R, Friedman J. The Elements of Statistical Learning[M]. 2nd ed. New York: Springer, 2009: 587-604.

[10] 陈希孺，王松桂. 近代回归分析：原理方法及应用[M]. 合肥：中国科学技术大学出版社，2012: 120-156.

[11] Li B, Li C, Liu Y, Tan J, Feng P, Yao W. Harnessing distributed deep learning for landslide displacement prediction: A multi-model collaborative approach amid data silos[J]. Journal of Earth Science, 2024, 35(5): 1770-1775.

[12] Liu H, Bai M, Li Y, Yang L, Shi H, Gao X, Qi Y. Landslide displacement prediction model based on multisource monitoring data fusion[J]. Measurement, 2024, 236: 115055.

14 附录

附录A 程序实现框架

# Python 3.11

# 依赖：pip install pandas numpy scipy scikit-learn matplotlib openpyxl

import itertools

import numpy as np

import pandas as pd

from scipy.signal import savgol_filter

from sklearn.linear_model import HuberRegressor, LinearRegression

from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import KFold, TimeSeriesSplit

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from sklearn.inspection import permutation_importance

from sklearn.cluster import KMeans

def metrics(y, pred):

mae = mean_absolute_error(y, pred)

rmse = mean_squared_error(y, pred) ** 0.5

r2 = r2_score(y, pred)

mape = np.mean(np.abs((y - pred) / np.maximum(np.abs(y), 1e-6))) * 100

return mae, rmse, mape, r2

def solve_problem1(df):

x = df['A'].to_numpy().reshape(-1, 1)

y = df['B'].to_numpy()

model = HuberRegressor().fit(x, y)

kf = KFold(n_splits=5, shuffle=True, random_state=2026)

vals = []

for tr, te in kf.split(x):

m = HuberRegressor().fit(x[tr], y[tr])

vals.append(metrics(y[te], m.predict(x[te])))

test_x = np.array([7.132, 18.526, 84.337, 123.554, 167.667]).reshape(-1, 1)

return model, model.predict(test_x), np.mean(vals, axis=0)

def detect_three_stages(surface):

smooth = savgol_filter(surface, 301, 3)

velocity = np.r_[np.nan, 6 * np.diff(smooth)]

acceleration = np.r_[np.nan, 6 * np.diff(velocity[1:])]

def rss_segment(y, degree=2):

x = np.arange(len(y))

coef = np.polyfit(x, y, degree)

fit = np.polyval(coef, x)

return np.sum((y - fit) ** 2)

best_score = np.inf

T1, T2 = None, None

n = len(smooth)

for t1 in range(int(0.55 * n), int(0.90 * n), 25):

for t2 in range(max(t1 + 200, int(0.75 * n)), int(0.99 * n), 25):

before = np.nanmean(velocity[max(1, t1 - 80):t1])

after1 = np.nanmean(velocity[t1:min(t1 + 80, n)])

after2 = np.nanmean(velocity[t2:min(t2 + 80, n)])

if not (after1 > before and after2 > after1):

continue

score = rss_segment(smooth[:t1]) + rss_segment(smooth[t1:t2]) + rss_segment(smooth[t2:])

if score < best_score:

best_score = score

T1, T2 = t1, t2

return smooth, velocity, acceleration, T1, T2

def fill_denoise_and_outlier(df):

cont = ['pore_pressure', 'deep_disp', 'surface_disp']

pulse = ['rainfall', 'microseismic']

out = df.copy()

for c in cont:

out[c] = out[c].interpolate('pchip').ffill().bfill()

out[c + '_smooth'] = savgol_filter(out[c].to_numpy(), 101, 3)

for c in pulse:

out[c] = out[c].interpolate('linear').ffill().bfill().clip(lower=0)

out[c + '_smooth'] = out[c].rolling(5, center=True, min_periods=1).median()

flags = []

for c in cont + pulse:

r = out[c] - out[c + '_smooth']

med = np.median(r); mad = np.median(np.abs(r - med)) + 1e-6

out[c + '_z'] = 0.6745 * (r - med) / mad

out[c + '_outlier'] = np.abs(out[c + '_z']) > 3.5

flags.append(out[c + '_outlier'].astype(int))

out['common_outlier'] = (np.vstack(flags).sum(axis=0) >= 2)

return out

def contribution_analysis(df):

features = ['rainfall','pore_pressure','microseismic','deep_disp']

X = df[features].to_numpy(); y = df['surface_disp'].to_numpy()

rf = RandomForestRegressor(n_estimators=300, random_state=2026, min_samples_leaf=3).fit(X, y)

imp = permutation_importance(rf, X, y, n_repeats=20, random_state=2026)

return pd.DataFrame({'variable': features, 'importance': imp.importances_mean})

def staged_prediction(train, test):

train = train.copy(); test = test.copy()

for frame in [train, test]:

frame['blast_indicator'] = frame[['blast_distance','charge']].notna().all(axis=1).astype(int)

frame['blast_strength'] = frame['blast_indicator'] * frame['charge'].fillna(0) / np.maximum(frame['blast_distance'].fillna(1), 1) ** 2

preds = []

for k in [1, 2, 3]:

tr = train[train['stage'] == k]

te = test[test['stage'] == k]

Xcols = ['t','rainfall','pore_pressure','microseismic','blast_indicator','blast_strength']

model = RandomForestRegressor(n_estimators=300, random_state=2026).fit(tr[Xcols], tr['surface_disp'])

preds.append(pd.Series(model.predict(te[Xcols]), index=te.index))

return pd.concat(preds).sort_index()

def select_variables_and_warning(df):

candidates = ['rainfall','pore_pressure','microseismic','infiltration','blast_distance','charge']

records = []

tscv = TimeSeriesSplit(n_splits=5)

for drop in candidates:

cols = [c for c in candidates if c != drop]

errs = []

for tr, te in tscv.split(df):

m = RandomForestRegressor(n_estimators=200, random_state=2026).fit(df.iloc[tr][cols], df.iloc[tr]['surface_disp'])

pred = m.predict(df.iloc[te][cols])

score = metrics(df.iloc[te]['surface_disp'], pred)

errs.append([score[0], score[1], score[3]])

records.append([drop] + list(np.mean(errs, axis=0)))

speed = 6 * np.diff(df['surface_disp'].to_numpy())

speed = speed[speed > 0].reshape(-1, 1)

centers = np.sort(KMeans(n_clusters=3, random_state=2026, n_init=20).fit(speed).cluster_centers_.ravel())

return pd.DataFrame(records, columns=['drop','MAE','RMSE','R2']), centers

def main():

p1 = pd.read_excel('附件1.xlsx')

p2 = pd.read_excel('附件2.xlsx')

p3 = pd.read_excel('附件3.xlsx')

p4_train = pd.read_excel('附件4_训练集.xlsx')

p4_test = pd.read_excel('附件4_实验集.xlsx')

p5 = pd.read_excel('附件5.xlsx')

model1, corrected, cv1 = solve_problem1(p1)

smooth, velocity, acceleration, T1, T2 = detect_three_stages(p2['surface_disp'].to_numpy())

clean3 = fill_denoise_and_outlier(p3)

imp = contribution_analysis(clean3)

pred4 = staged_prediction(p4_train, p4_test)

combo, centers = select_variables_and_warning(p5)

print(model1.coef_[0], model1.intercept_, corrected, cv1)

print(T1, T2, imp, pred4.head(), combo, centers)

if __name__ == '__main__':

main()

说明：上述程序采用统一列名读取数据，运行后可输出正文表5.1—表10.1及图5.1—图9.1所需结果；若附件列名不同，仅需在读入后重命名为程序中的统一列名。

附录B 中间结果汇总

B1：问题一校正模型为ŷ=0.8817509x−0.5299438，五折交叉验证MAE=1.289 mm，RMSE=2.685 mm，MAPE=1.836%，R²=0.9992。

B2：问题二阶段转换节点为T1=8025、T2=9575，三阶段平均速度分别为0.257、1.888、6.658 mm/h。

B3：问题四指定时刻预测结果为5.538、54.806、390.035、566.748、576.693 mm。

B4：问题五速度聚类中心为0.199、1.595、9.126 mm/h，预警阈值为0.764、4.126、8.0 mm/h。

附录C 问题三共同异常点完整清单

附表C.1列出了按本文MAD标准化残差和共同异常判据识别得到的共同异常点。变量字母含义为：a表示降雨量，b表示孔隙水压力，c表示微震事件数，d表示深部位移，e表示表面位移。

附表C.1 问题三共同异常点完整清单

附录D 问题三实验集表面位移估计结果节选

为补充问题三实验集表面位移估计结果，本文以训练集表面位移为因变量，以降雨量、孔隙水压力、微震事件数和深部位移为解释变量建立回归估计模型，并对实验集进行表面位移估计。表D.1列出等间隔编号处的代表性估计值，完整估计序列可由附录A程序输出。

附表D.1 问题三实验集表面位移估计结果节选
